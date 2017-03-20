



class IrSequence(models.Model):
    _name = 'ir.sequence'

        def seq_date_range = self.env['ir.sequence.date_range'].sudo().create({
            'date_from': date_from,
            'date_to': date_to,
            'sequence_id': self.id,

        def _create_date_range_seq(self, date):
            year = fields.Date.from_string(date).strftime('%Y')
            date_from = '{}-01-01'.format(year)
            date_to = '{}-12-31'.format(year)
            date_range = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_from', '>=', date), ('date_from', '<=', date_to)], order='date_from desc')
            if date_range:
                date_to = datetime.strptime(date_range.date_from, '%Y-%m-%d') + timedelta(days=-1)
                date_to = date_to.strftime('%Y-%m-%d')
                date_range = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_to', '>=', date_from), ('date_to', '<=', date)], order='date_to desc')
            if date_range:
                date_from = datetime.strptime(date_range.date_to, '%Y-%m-%d') + timedelta(days=1)
                date_from = date_from.strftime('%Y-%m-%d')
                seq_date_range = self.env['ir.sequence.date_range'].sudo().create({
                'date_from': date_from,
                'date_to': date_to,
                'sequence_id': self.id,
            })
        return seq_date_range