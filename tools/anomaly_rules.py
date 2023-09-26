def calculate_average(data):
  total = len(data)
  response = {
    "avg_failed": 0,
    "avg_reversed": 0,
    "avg_denied": 0
  }
  for log in data:
    response["avg_denied"] += log["denied"]
    response["avg_reversed"] += log["reversed"]
    response["avg_failed"] += log["failed"]
  response["avg_denied"] = response["avg_denied"] / total
  response["avg_reversed"] = response["avg_reversed"] / total
  response["avg_failed"] = response["avg_failed"] / total
  return response

def check_transactions(data):
  data_to_check = data[-1]
  total = data_to_check["approved"] + data_to_check["backend_reversed"] + data_to_check["denied"] + data_to_check["failed"] + data_to_check["processing"] + data_to_check["refunded"] + data_to_check["reversed"]
  
  ### CHANGE VARIABLE RULES HERE ##
  err_transactions_perc_critical_index = 50
  err_transactions_perc_warning_index = 20
  
  # alert if failed + denied + reversed are higher than [err_transactions_perc_critical_index]% of transactions
  error_percentage = ((data_to_check["failed"] + data_to_check["denied"] + data_to_check["reversed"]) / total) * 100
  if error_percentage > err_transactions_perc_critical_index:
    return { "alert": "CRITIC: Failed, denied and reversed values are higher than 50 percent of all transactions", "level": error_percentage, "history": data }
  
  # alert if failed, denied or reversed above it's historical average and higher
  # than [err_transactions_perc_warning_index]% of transactions
  elif error_percentage > err_transactions_perc_warning_index:
    avg_history = calculate_average(data)
    if data_to_check["failed"] > avg_history["avg_failed"]:
      fail_level = ((data_to_check["failed"] - avg_history["avg_failed"]) / avg_history["avg_failed"]) * 100
      return { "alert": "Warning: Failed transactions are above average", "level": fail_level, "history": data }
    if data_to_check["denied"] > avg_history["avg_denied"]:
      deny_level = ((data_to_check["denied"] - avg_history["avg_denied"]) / avg_history["avg_denied"]) * 100
      return { "alert": "Warning: Denied transactions are above average", "level": deny_level, "history": data }
    if data_to_check["reversed"] > avg_history["avg_reversed"]:
      reverse_level = ((data_to_check["reversed"] - avg_history["avg_reversed"]) / avg_history["avg_reversed"]) * 100
      return { "alert": "Warning: Reversed transactions are above average", "level": reverse_level, "history": data }
  
  return { "history": data }