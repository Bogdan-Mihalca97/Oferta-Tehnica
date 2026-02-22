"""
Flask Blueprint for PTE (Proceduri Tehnice de Executie) generation.
Fetches PDF from Creatio, generates PTE via Claude, uploads DOCX back to Creatio.
"""
import os
import tempfile

import fitz  # PyMuPDF
from flask import Blueprint, request, jsonify, current_app

from app import generate_pte, build_docx
from config.config import anthropic_api_key

MODEL = 'claude-opus-4-6'

propunere_tehnica_bp = Blueprint(
    'propunere_tehnica',
    __name__,
    url_prefix='/cx-ai/propunere-tehnica'
)


@propunere_tehnica_bp.route('/proceduri-tehnice-de-executie', methods=['POST'])
def generate_proceduri_tehnice_de_executie():
    try:
        body = request.get_json(force=True, silent=True) or {}
        record_id = body.get('RecordId')
        doc_id = body.get('DocId')

        if not record_id or not doc_id:
            missing = [f for f, v in [('RecordId', record_id), ('DocId', doc_id)] if not v]
            return jsonify({'success': False, 'error': f"Missing required fields: {', '.join(missing)}"}), 400

        file_service = current_app.config['creatio_file_service']

        # Step 1: Download PDF bytes from Creatio
        try:
            pdf_bytes = file_service.download_file(doc_id)
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to download PDF from Creatio: {e}"}), 500

        # Step 2: Extract text from PDF bytes (in-memory, no temp file)
        try:
            doc = fitz.open(stream=pdf_bytes, filetype='pdf')
            pages = [doc[i].get_text() for i in range(len(doc))]
            doc.close()
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to extract PDF text: {e}"}), 500

        # Step 3: Generate PTE text via Claude API
        try:
            pte_text, in_tok, out_tok = generate_pte(pages, api_key=anthropic_api_key, model=MODEL)
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to generate PTE via Claude: {e}"}), 500

        # Step 4: Build DOCX to a temp file
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
                tmp_path = tmp.name
            build_docx(pte_text, tmp_path)
            with open(tmp_path, 'rb') as f:
                docx_bytes = f.read()
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to build DOCX: {e}"}), 500
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Step 5: Upload DOCX to Creatio
        try:
            file_service.upload_file(record_id, 'proceduri_tehnice_executie.docx', docx_bytes)
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to upload DOCX to Creatio: {e}"}), 500

        return jsonify({
            'success': True,
            'inputTokens': in_tok,
            'outputTokens': out_tok,
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
