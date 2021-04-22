from dateutil.parser import parse as date_parse


def get_block_number(block):
	return int(block['blockV1']['payload']['height'])


def get_signatures(block):
	return block['blockV1']['signatures']


def get_id(block):
	return block['id']


def get_creation_date(block):
	return date_parse(block['dateTimeFormatted'])


def get_transactions_count(block):
	return block['lengthTransactions']
