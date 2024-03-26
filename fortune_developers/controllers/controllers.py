# -*- coding: utf-8 -*-
# from odoo import http


# class FortuneDevelopers(http.Controller):
#     @http.route('/fortune_developers/fortune_developers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fortune_developers/fortune_developers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fortune_developers.listing', {
#             'root': '/fortune_developers/fortune_developers',
#             'objects': http.request.env['fortune_developers.fortune_developers'].search([]),
#         })

#     @http.route('/fortune_developers/fortune_developers/objects/<model("fortune_developers.fortune_developers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fortune_developers.object', {
#             'object': obj
#         })

