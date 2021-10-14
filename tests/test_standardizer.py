from scielo_scholarly_data.standardizer import (
    document_author,
    document_doi,
    document_first_page,
    document_title_for_deduplication,
    document_title_for_visualization,
    journal_issn,
    journal_title_for_deduplication,
    journal_title_for_visualization,
    issue_number,
    issue_volume
)

import unittest


class TestStandardizer(unittest.TestCase):

    def test_journal_title_for_deduplication_html_code_to_unicode(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia &amp; (Uruguay)'),
            'agrociencia & uruguay'
        )


    def test_journal_title_for_deduplication_remove_nonprintable_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay)\n'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_parentheses_and_content(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay)', keep_parenthesis_content=False),
            'agrociencia'
        )

    def test_journal_title_for_deduplication_remove_accentuation(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociência (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_convert_to_alphanumeric_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia + (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_double_space(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia    (Uruguay)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_remove_special_words(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (Uruguay) online'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_deduplication_to_lowercase_char(self):
        self.assertEqual(
            journal_title_for_deduplication('Agrociencia (URUGUAY)'),
            'agrociencia uruguay'
        )

    def test_journal_title_for_visualization_html_code_to_unicode(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia &amp; (Uruguay)'),
            'Agrociencia & (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_nonprintable_char(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia (Uruguay)\n'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_double_space(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia    (Uruguay)'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_title_for_visualization_remove_pointing_at_end(self):
        self.assertEqual(
            journal_title_for_visualization('Agrociencia (Uruguay).,;'),
            'Agrociencia (Uruguay)'
        )

    def test_journal_issn_without_hyphen(self):
        issns = {
            '15856280': '1585-6280',
            '85856281': '8585-6281'
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_correct(self):
        issns = {
            '1585-6280': '1585-6280',
            '8585-6281': '8585-6281'
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_char(self):
        issns = {
            '1585x6280': None,
            '85856281a': None,
            '8585-62s81': None,
            'x8585-6281': None,
            '85X856281': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_space(self):
        issns = {
            '1585 6280': None,
            '85856281 ': None,
            ' 8585-6281': None,
            '85 85-6281': None,
            '8585 6281 ': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_journal_issn_with_less_or_more_positions(self):
        issns = {
            '185-6280': None,
            '8585-281': None,
            '8585-628': None,
            '8685-62833': None,
            '85835-6282': None,
            '808-63286': None
        }

        expected_values = list(issns.values())
        obtained_values = [journal_issn(i) for i in issns]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_doi(self):
        dois = {
            'https://10.1016/J.SCITOTENV.2019.02.108': '10.1016/J.SCITOTENV.2019.02.108',
            'http://10.1007/S13157-019-01161-Y': '10.1007/S13157-019-01161-Y',
            '10.4257/OECO.2020.2401.05': '10.4257/OECO.2020.2401.05',
            'ftp://10.1111/EFF.12536': '10.1111/EFF.12536',
            'axc; 10.1007/S10452-020-09782-W': '10.1007/S10452-020-09782-W',
            '&referrer=google*url=10.1590/1678-4766E2016006': '10.1590/1678-4766E2016006',
        }

        expected_values = list(dois.values())
        obtained_values = [document_doi(d) for d in dois]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_author(self):
        authors = {
            'Silva, Joao  J. P.. &': 'Silva Joao J P',
            'Santos;=;] R': 'Santos R',
            'Joao...Paulo': 'Joao Paulo',
            '3ø Elton Jonas': 'Elton Jonas',
            'Elvis-Presley': 'Elvis Presley'
        }

        expected_values = list(authors.values())
        obtained_values = [document_author(da) for da in authors]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_first_page_unescape(self):
        self.assertEqual(
            document_first_page('12&#60;8'),
            '128'
        )

    def test_document_first_page_non_printable_chars(self):
        self.assertEqual(
            document_first_page('12\n8'),
            '128'
        )

    def test_document_first_page_alpha_num_space(self):
        self.assertEqual(
            document_first_page('12&8'),
            '128'
        )

    def test_document_first_page_double_spaces(self):
        self.assertEqual(
            document_first_page('  12  8'),
            '128'
        )

    def test_document_first_page_end_punctuation_chars(self):
        self.assertEqual(
            document_first_page('128.,; .'),
            '128'
        )

    def test_document_first_page_range(self):
        range = {
            '128-140': '128',
            '128_140': '128',
            '128:140': '128',
            '128;140': '128',
            '128,140': '128',
            '128.140': '128'
        }
        expected_values = list(range.values())
        obtained_values = [document_first_page(page) for page in range]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_special_char(self):
        issues = {
            '&96':'96',
            '$96':'96',
            '@96a':'96a',
            '!96a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_non_printable(self):
        issues = {
            '\n96':'96',
            '96\t':'96',
            '96\aa':'96a',
            '9\n6a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_with_spaces(self):
        issues = {
            ' 96':'96',
            '96  ':'96',
            '96 a ':'96 a',
            ' 96 a':'96 a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_number_with_parenthesis(self):
        issues = {
            '(96)':'96',
            '9(6)':'96',
            '96(a)':'96a',
            '(96)a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_number(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_special_char(self):
        issues = {
            '&96':'96',
            '$96':'96',
            '@96a':'96a',
            '!96a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_non_printable(self):
        issues = {
            '\n96':'96',
            '96\t':'96',
            '96\aa':'96a',
            '9\n6a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_spaces(self):
        issues = {
            ' 96':'96',
            '96  ':'96',
            '96 a ':'96 a',
            ' 96 a':'96 a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_with_parenthesis(self):
        issues = {
            '(96)':'96',
            '9(6)':'96',
            '96(a)':'96a',
            '(96)a':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_issue_volume_remove_points_at_end(self):
        issues = {
            '(96).':'96',
            '9(6);':'96',
            '96(a),':'96a',
            '(96)a .':'96a'
        }
        expected_values = list(issues.values())
        obtained_values = [issue_volume(num) for num in issues]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_deduplication_html_entities_keeps(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS', remove_special_char=False),
            'innovacion tecnologica en la resolucion de < problematicas'
        )

    def test_document_title_for_deduplication_keep_alpha_num_space(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN & TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_non_printable_chars(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN \n TECNOLÓGICA EN LA RESOLUCIÓN DE \t PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_double_spaces(self):
        self.assertEqual(
            document_title_for_deduplication('  INNOVACIÓN  TECNOLÓGICA  EN  LA  RESOLUCIÓN  DE  PROBLEMÁTICAS  '),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_end_punctuation_chars(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS,.;'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_text_strip(self):
        self.assertEqual(
            document_title_for_deduplication(' INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS '),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_remove_accents(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_deduplication_text_lower(self):
        self.assertEqual(
            document_title_for_deduplication('INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'),
            'innovacion tecnologica en la resolucion de problematicas'
        )

    def test_document_title_for_visualization_html_entities_keeps(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#60; PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE < PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE &#163; PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE £ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt, remove_special_char=False) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_non_printable(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \n PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \t PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE \a PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DE PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_alpha_num_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ: PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ* PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ& PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_double_spaces(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ  PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ   PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ    PROBLEMÁTICAS':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)

    def test_document_title_for_visualization_remove_pointing_at_end(self):
        titles = {
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS..':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÊ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS.,;':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DẼ PROBLEMÁTICAS',
            'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS,,,,':
                'INNOVACIÓN TECNOLÓGICA EN LA RESOLUCIÓN DÈ PROBLEMÁTICAS'
        }
        expected_values = list(titles.values())
        obtained_values = [document_title_for_visualization(dt) for dt in titles]

        self.assertListEqual(expected_values, obtained_values)