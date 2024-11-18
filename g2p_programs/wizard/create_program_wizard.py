# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
import logging
from uuid import uuid4

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class G2PCreateNewProgramWiz(models.TransientModel):
    _name = "g2p.program.create.wizard"
    _inherit = ["base.programs.manager", "g2p.cycle.recurrence.mixin"]
    _description = "Create a New Program Wizard"

    name = fields.Char("Program Name", required=True)
    currency_id = fields.Many2one("res.currency", "Currency", required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    eligibility_domain = fields.Text(string="Domain", default="[]", required=True)
    target_type = fields.Selection(
        [
            ("group", "Group"),
            ("individual", "Individual"),
            ("family", "Family")  # New option added
        ],
        default="group",
    )
    import_beneficiaries = fields.Selection([("yes", "Yes"), ("no", "No")], default="no")
    state = fields.Selection(
        [("step1", "Set Defaults"), ("step2", "Import Registrants")],
        "Status",
        default="step1",
        readonly=True,
    )

    def create_program(self):
        # Logic to create the program
        pass
