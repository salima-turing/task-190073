import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_data(data_file, validation_rules):
	try:
		# Read the data
		data = pd.read_csv(data_file)

		for col_name, rules in validation_rules.items():
			if col_name in data.columns:
				logger.info(f"Validating column: {col_name}")
				for rule_name, rule_func in rules.items():
					is_valid = rule_func(data[col_name])
					if not is_valid:
						logger.error(f"Validation failed for {col_name}: {rule_name}")
			else:
				logger.error(f"Column '{col_name}' not found in the data.")

	except Exception as e:
		logger.error(f"An error occurred: {e}")


def is_non_empty(series):
	return not series.isnull().any() and not series.eq('').any()

def is_integer(series):
	try:
		series.astype(int)
		return True
	except ValueError:
		return False

def is_in_range(series, min_value, max_value):
	return (series >= min_value) & (series <= max_value)


if __name__ == "__main__":
	data_file_path = 'dummy_data.csv'

	validation_rules = {
		"Client_ID": {
			"Non-empty": is_non_empty,
			"Integer": is_integer
		},
		"Age": {
			"Non-empty": is_non_empty,
			"Integer": is_integer,
			"Range": lambda series: is_in_range(series, 18, 150)
		},
		"Email": {
			"Non-empty": is_non_empty,
		},
		"Document_Type": {
			"Non-empty": is_non_empty,
			"Allowed_values": lambda series: series.isin(["Passport", "ID Card", "Driver's License"])
		},
	}

	validate_data(data_file_path, validation_rules)
