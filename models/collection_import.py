from odoo import models, fields, api
import requests

class CollectionImport(models.Model):
    _name = 'collection.import'
    _description = 'Import Collections from Rails'

    api_token = fields.Char(string="API Token", required=True)

    @api.model
    def import_collections(self):
        tokens = self.env['x_api_token'].search([])
        for token in tokens:
            url = "https://treasurex.onrender.com/api/v1/collections"
            headers = {
                "Authorization": f"Bearer {token.api_token}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                collections = response.json()
                collection_model = self.env['x_collection']
                for collection in collections:
                    collection_model.create({
                        'name': collection['name'],
                        'description': collection['description'],
                        'number_of_items': collection['item_count'],
                        'category': collection['category_id']
                    })
                log_message = "Collections imported successfully"
                status = "success"
            else:
                log_message = f"Failed to fetch collections: {response.text}"
                status = "failure"

            self.env['x_import_log'].create({
                'log_message': log_message,
                'status': status,
                'timestamp': fields.Datetime.now(),
            })
