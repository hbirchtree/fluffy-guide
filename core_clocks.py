from common import *

def core_enumerator() -> Iterator[CoreDescription]:
    procs = glob('/sys/bus/cpu/devices/cpu*')

    i = 0

    for proc in procs:
        max_clk = read_int('%s/cpufreq/scaling_max_freq' % proc) / 1000
        min_clk = read_int('%s/cpufreq/scaling_min_freq' % proc) / 1000
        cur_clk = read_int('%s/cpufreq/scaling_cur_freq' % proc) / 1000
        node = glob('%s/node*' % proc)
        if len(node) > 0:
            node = node[0].replace('%s' % proc, '').replace('/', '')
        else:
            node = 'node0'
        gov = read_string('%s/cpufreq/scaling_governor' % proc)\
            .replace('\n', '')
        av_govs = read_string('%s/cpufreq/scaling_available_governors' % proc)\
            .replace('\n', '').split(' ')
        yield CoreDescription(max_clk, cur_clk, min_clk, node, gov, av_govs,
                              'Core %s' % i)
        i += 1


def system_description() -> SystemDescription:
    plat_data = uname()
    dist = (plat_data.system, plat_data.release)
    for opt in (linux_distribution(), win32_ver(), mac_ver()):
        if len(opt[0]) > 0:
            dist = opt
            break
    return SystemDescription(plat_data.system,
                             plat_data.release,
                             plat_data.machine,
                             dist[0], dist[1])


def processor_description() -> ProcessorDescription:
    try:
        proc_info = read_string('/proc/cpuinfo')

        proc_info = proc_info.split('\n')
        proc_map = {}

        for i, e in enumerate(proc_info):
            proc_info[i] = e.split(':')
            if len(proc_info[i]) < 2:
                continue
            for j,n in enumerate(proc_info[i]):
                proc_info[i][j] = n.strip()
            proc_map[proc_info[i][0]] = proc_info[i][1]

        try:
            return ProcessorDescription(proc_map['vendor_id'],
                                        proc_map['model name'],
                                        uname().machine)
        except KeyError:
            return ProcessorDescription(proc_map['model name'],
                                        proc_map['Hardware'],
                                        uname().machine)
    except FileNotFoundError:
        return ProcessorDescription('Generic', 'Processor', '???')