from common import *


def hwmon_enumerator() -> Iterator[HWMonSensor]:
    def read_temp(fn: str):
        return read_float(fn) / 1000.0

    hwmon_sensors = glob('/sys/class/hwmon/*')
    for sensor in hwmon_sensors:
        input_files = glob('%s/temp*_input' % (sensor,))
        max_files = glob('%s/temp*_max' % (sensor,))
        crit_files = glob('%s/temp*_crit' % (sensor,))
        label_files = glob('%s/temp*_label' % (sensor,))

        for inp, mx, crt, lab in zip(input_files,
                                     max_files,
                                     crit_files,
                                     label_files):
            yield HWMonSensor(read_stringnl(lab),
                              basename(sensor),
                              read_temp(inp), read_temp(mx),
                              read_temp(crt))