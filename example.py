import rotary_encoder

last = 0

e = rotary_encoder.Encoder(12, 16)

while True:  # Infinite loop
    value = e.get_value()  # Get rotary encoder value
    if value != last:  # If there is a new value do
        last = value
        print(value)  # In this case it prints the value
