import hashlib
test = "levi"

hash_val = hashlib.sha384(test.encode()).hexdigest()
print("SHA384: ", hash_val)

