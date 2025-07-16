#!/usr/bin/env python3

"""
split_letter_legal.py
Splits a PDF into two PDFs: one with Letter-sized pages and one with Legal-sized pages.
"""

from PyPDF2 import PdfReader, PdfWriter
import os
import argparse

def split_pdf(input_path, letter_out, legal_out):
    reader = PdfReader(input_path)
    letter_writer = PdfWriter()
    legal_writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)

        if abs(h - 792) < 5:  # Letter (8.5x11")
            letter_writer.add_page(page)
        elif abs(h - 1008) < 5:  # Legal (8.5x14")
            legal_writer.add_page(page)
        else:
            print(f"⚠️ Page {i+1} has unknown size: {w} x {h}")

    if letter_writer.get_num_pages() > 0:
        with open(letter_out, "wb") as f:
            letter_writer.write(f)
        print(f"✅ Letter-sized pages saved to: {letter_out}")
    else:
        print("ℹ️ No Letter-sized pages found.")

    if legal_writer.get_num_pages() > 0:
        with open(legal_out, "wb") as f:
            legal_writer.write(f)
        print(f"✅ Legal-sized pages saved to: {legal_out}")
    else:
        print("ℹ️ No Legal-sized pages found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a PDF into Letter and Legal-sized pages.")
    parser.add_argument("input", help="Path to input PDF")
    parser.add_argument("--letter", default="letter_pages.pdf", help="Output file for Letter pages")
    parser.add_argument("--legal", default="legal_pages.pdf", help="Output file for Legal pages")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"❌ Input file not found: {args.input}")
        exit(1)

    split_pdf(args.input, args.letter, args.legal)

