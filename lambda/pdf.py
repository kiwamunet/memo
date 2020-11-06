import tempfile

import pdfkit
import PyPDF2
import os


class PDFGenerator:
    contents = ""

    def generate(self, html_contents, landscape=True, options=None):

        default_options = {
            "page-size": "A4",
            "orientation": "Landscape",
            "margin-top": "0.1in",
            "margin-right": "0.1in",
            "margin-bottom": "0.1in",
            "margin-left": "0.1in",
            "encoding": "UTF-8",
            "no-outline": None,
            "quiet": "",
            "load-media-error-handling": "ignore",
        }

        if not landscape:
            default_options.pop("orientation")

        if options is not None:
            options = dict(default_options, **options)
        else:
            options = default_options

        try:
            self.contents = pdfkit.from_string(
                html_contents, False, options=options)
            if self.contents == "":
                assert False, f"PDFコンテンツが空です {template}"
            else:
                return html_contents
        except IOError as e:
            assert False, f"IOエラーが発生しました {str(e)}"

    def get_contents(self):
        return self.contents

    def save(self, name="", mode="wb"):
        with open(name, mode=mode) as fp:
            fp.write(self.get_contents())
        return name
