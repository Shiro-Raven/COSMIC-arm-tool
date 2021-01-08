import re


def get_cfps(inst_name, params):
    entries_num = len(params)

    entries = 0
    reads = 0
    writes = 0

    if inst_name == 'push':
        entries = 1
        reads = entries_num
        writes = entries_num
    elif inst_name == 'pop' or inst_name == 'popne' or inst_name == 'popeq':
        entries = 1
        reads = entries_num
        writes = entries_num
    elif inst_name == 'add':
        entries = 5
        reads = 2
        writes = 1
    elif inst_name == 'sub':
        entries = 3
        reads = 2
        writes = 1
    elif inst_name == 'mul':
        reads = 2
        writes = 1
    elif inst_name == 'mov' or inst_name == 'asr' or inst_name == 'asrs':
        entries = 2
        reads = 0 if entries_num == 1 else 1
        writes = 1
    elif inst_name == 'ldr' or inst_name == 'ldrb':
        entries = 3
        reads = 2
        writes = 1
    elif inst_name == 'cmp':
        entries = 2 if entries_num == 1 else 4
        reads = 1 if entries_num == 1 else 2
        writes = 1
    elif inst_name == 'b' or inst_name == 'bne':
        entries = 1
        reads = 0
        writes = 1
    elif inst_name == 'bl' or inst_name == 'blx':
        entries = 1
        reads = 1 if params[0].startswith('r') else 0
        writes = 2 if inst_name.endswith('x') else 1
    elif inst_name == 'bx' or inst_name == 'bxeq':
        entries = 1
        reads = 1
        writes = 2
    elif inst_name == 'str' or inst_name == 'strb':
        entries = 3
        reads = 2
        writes = 1
    else:
        raise Exception('Undefined Instruction:', inst_name)

    return entries, reads, writes


def analyse(text_file_path):
    text = open(text_file_path, 'r')

    instructions = list()
    unique_inst = dict()

    total_entries = 0
    total_writes = 0
    total_reads = 0

    for line in text:
        split = line.split('\t')
        if len(split) >= 4 and split[0].endswith(':') and re.search("[^a-f0-9.]", split[0]):
            if (split[2] == '.word'):
                continue

            inst_hex = split[1].strip()
            inst_name = split[2]
            ops = ' '.join(split[3:]).strip()
            ops = ops.split(';')[0].strip()

            params = ops.replace('[', '').replace(']', '').replace('{', '').replace(
                '}', '').replace('(', '').replace(')', '').replace(';', ',').split(',')
            params = [entry.strip() for entry in params]
            params = [entry for entry in params if not (entry.startswith(
                '#') or entry.startswith('0x') or entry.isnumeric())]

            entries, reads, writes = get_cfps(inst_name, params)
            entries += 1
            exits = 0

            total_entries += entries
            total_reads += reads
            total_writes += writes

            if inst_name not in unique_inst:
                unique_inst[inst_name] = entries + reads + writes + 1
            else:
                unique_inst[inst_name] += entries + reads + writes + 1

            instructions.append(
                (inst_hex, inst_name, '"' + str(ops) + '"', str(entries), str(reads), str(writes), str(exits)))

    return instructions, unique_inst, (total_entries, total_reads, total_writes)

