def calculate_average(data):
  total = len(data)
  response = {
    "avg_approved": 0,
    "avg_backend_reversed": 0,
    "avg_denied": 0,
    "avg_failed": 0,
    "avg_reversed": 0
  }
  for log in data:
    response["avg_approved"] += log["approved"]
    response["avg_backend_reversed"] += log["backend_reversed"]
    response["avg_denied"] += log["denied"]
    response["avg_failed"] += log["failed"]
    response["avg_reversed"] += log["reversed"]
  for tag in response:
    response[tag] = response[tag] / total
  return response

def check_transactions(data):
  data_to_check = data[-1]
  total = data_to_check["approved"] + data_to_check["backend_reversed"] + data_to_check["denied"] + data_to_check["failed"] + data_to_check["refunded"] + data_to_check["reversed"]
  
  ### CHANGE VARIABLE RULES HERE ##
  err_transactions_perc_critical_index = 20
  err_transactions_perc_warning_index = 3.52
  
  # alert if failed + denied + reversed are higher than [err_transactions_perc_critical_index]% of transactions
  error_percentage = ((data_to_check["failed"] + data_to_check["reversed"]) / total) * 100
  if error_percentage > err_transactions_perc_critical_index:
    return { "alert": f"CRITICAL: Failed and/or reversed values are higher than {err_transactions_perc_critical_index}% of all transactions", "level": error_percentage, "history": data }
  
  # alert if failed, denied or reversed above it's historical average and higher
  # than [err_transactions_perc_warning_index]% of transactions
  elif error_percentage > err_transactions_perc_warning_index:
    avg_history = calculate_average(data)
    if data_to_check["failed"] > avg_history["avg_failed"]:
      fail_level = ((data_to_check["failed"] - avg_history["avg_failed"]) / avg_history["avg_failed"]) * 100
      return { "alert": f"Warning: Failed transactions are {round(fail_level, 2)}% above history average", "level": fail_level, "history": data }
    if data_to_check["reversed"] > avg_history["avg_reversed"]:
      fail_level = ((data_to_check["reversed"] - avg_history["avg_reversed"]) / avg_history["avg_reversed"]) * 100
      return { "alert": f"Warning: Reversed transactions are {round(fail_level, 2)}% above history average", "level": fail_level, "history": data }
    if data_to_check["denied"] > avg_history["avg_denied"]:
      fail_level = ((data_to_check["denied"] - avg_history["avg_denied"]) / avg_history["avg_denied"]) * 100
      return { "alert": f"Warning: Denied transactions are {round(fail_level, 2)}% above history average", "level": fail_level, "history": data }
  
  return { "history": data }