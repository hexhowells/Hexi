import time
from ads1015 import ADS1015


class Battery:
    def __init__(self, channel = 'in0/ref'):
        self.channel = channel
        self.ads = ADS1015()
        self.chip_type = self.ads.detect_chip_type()
        self.ads.set_mode("single")
        self.ads.set_programmable_gain(2.048)

        if self.chip_type == "ADS1015":
            self.ads.set_sample_rate(1600)
        else:
            self.ads.set_sample_rate(860)

        self.reference = self.ads.get_reference_voltage()

    def voltage(self):
        time.sleep(0.5)
        samples = 5 
        avg_voltage = 0

        for i in range(samples):
            avg_voltage += self.ads.get_compensated_voltage(
                                    channel=self.channel, 
                                    reference_voltage=self.reference
                                    )

        voltage = avg_voltage / samples

        return round(voltage, 3)


    def percentage(self, min_v=3.3, max_v=3.7):
        voltage = self.voltage()
        normalised_v = max(0, voltage - min_v)
        normalised_max_v = max_v - min_v

        percentage = int((normalised_v / normalised_max_v) * 100)

        return percentage
