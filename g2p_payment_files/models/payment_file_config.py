import pdfkit

from odoo import fields, models


class G2PPaymentFileConfig(models.Model):
    _name = "g2p.payment.file.config"
    _description = "Payment File Config"
    _order = "id desc"

    name = fields.Char()

    type = fields.Selection(
        [
            ("pdf", "PDF"),
            ("csv", "CSV"),
        ],
        default="pdf",
    )

    body_string = fields.Text(string="Body")

    qrcode_config_ids = fields.One2many("g2p.payment.file.qrcode.config", "payment_config_id")

    # Function to render and store generated files
    def render_and_store(self, res_model, res_ids, document_store):
        """
        Render templates for multiple records and store the output as files.
        Args:
            res_model (str): Model name of the record.
            res_ids (list): List of record IDs to process.
            document_store (object): File storage object where the generated files will be saved.

        Returns:
            list: A list of document file references added to the document store.
        """
        document_files = []
        for res_id in res_ids:
            document_files.append(
                document_store.add_file(self.render_template(res_model, res_id), extension="." + self.type)
            )
        return document_files

    # Function to render a template for a specific record
    def render_template(self, res_model, res_id):
        """
        Render a template for a specific record.
        Args:
            res_model (str): Model name of the record.
            res_id (int): ID of the record to process.

        Returns:
            bytes: Rendered content in the format specified by the `type` field.
        """
        if self.type == "pdf":
            return self.render_pdf(res_model, res_id)
        elif self.type == "csv":
            return self.render_csv(res_model, res_id)

    # Function to render HTML for a specific record
    def render_html(self, res_model, res_id):
        """
        Render an HTML template for a specific record.
        Args:
            res_model (str): Model name of the record.
            res_id (int): ID of the record to process.

        Returns:
            str: Rendered HTML content.
        """
        RenderMixin = self.env["mail.render.mixin"]
        template_src = self.body_string
        data = RenderMixin._render_template(
            template_src,
            res_model,
            [
                res_id,
            ],
            engine="qweb",
        )
        # This render_template removes <html> and <head> content.
        return data[res_id]

    # Function to render and return a PDF file
    def render_pdf(self, res_model, res_id):
        """
        Render a PDF file using the HTML content of a specific record.
        Args:
            res_model (str): Model name of the record.
            res_id (int): ID of the record to process.

        Returns:
            bytes: Rendered PDF content.
        """
        res = self.render_html(res_model, res_id)
        return pdfkit.from_string(res)

    # Function to render and return a CSV file
    def render_csv(self, res_model, res_id):
        """
        Render a CSV file using the HTML content of a specific record.
        Args:
            res_model (str): Model name of the record.
            res_id (int): ID of the record to process.

        Returns:
            bytes: Rendered CSV content.
        """
        return bytes(self.render_html(res_model, res_id), "utf-8")
