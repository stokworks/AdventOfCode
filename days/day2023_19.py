from copy import deepcopy
import math
import operator

from days import AOCDay, day


@day(2023, 19)
class Day2023_19(AOCDay):
    test_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".split('\n')

    parts = []
    flows = dict()

    def test(self, input_data):
        self.common(self.test_input)
        assert self.part1(self.test_input) == 19114
        assert self.part2(self.test_input) == 167409079868000

    def common(self, input_data):
        self.parts = []
        self.flows = dict()

        reading_flows = True

        for line in input_data:
            if reading_flows:
                if len(line) == 0:
                    reading_flows = False
                    continue

                flow_name = line[:line.index('{')]
                rules = []
                for rule in line[line.index('{') + 1:-1].split(','):
                    if ':' in rule:
                        rules.append((
                            rule[0],
                            rule[1],
                            int(rule[2:rule.index(':')]),
                            rule[rule.index(':') + 1:]
                        ))
                    else:
                        rules.append((rule,))
                self.flows[flow_name] = rules
            else:
                part = dict()
                for category in line[1:-1].split(','):
                    part[category[0]] = int(category[2:])
                self.parts.append(part)

    def part1(self, input_data):
        acc = 0

        for part in self.parts:
            flow = self.flows['in']

            is_accepted = False
            is_rejected = False

            while not is_accepted and not is_rejected:
                for rule in flow:
                    target = None

                    if len(rule) == 1:
                        target = rule[0]
                    else:
                        category, op, test, goto = rule

                        if (operator.lt if op == '<' else operator.gt)(part[category], test):
                            target = goto

                    if target:
                        if target not in 'AR':
                            flow = self.flows[target]
                        is_accepted = target == 'A'
                        is_rejected = target == 'R'
                        break

            if is_accepted:
                acc += sum(part.values())

        return acc

    def part2(self, input_data):
        def count_combinations(workflow, values_intervals):
            if workflow == 'A':
                return math.prod([len(r) for r in values_intervals.values()])
            if workflow == 'R':
                return 0

            acc = 0
            for rule in self.flows[workflow]:
                if len(rule) == 1:
                    target = rule[0]
                    acc += count_combinations(target, values_intervals)
                    break

                category, op, test, target = rule

                if op == '<':
                    branch_accepted = range(values_intervals[category].start, test)
                    branch_rejected = range(test, values_intervals[category].stop)
                else:
                    branch_accepted = range(test + 1, values_intervals[category].stop)
                    branch_rejected = range(values_intervals[category].start, test + 1)

                accepted_intervals = deepcopy(values_intervals)
                accepted_intervals[category] = branch_accepted
                values_intervals[category] = branch_rejected
                acc += count_combinations(target, accepted_intervals)

            return acc

        values_intervals = {category: range(1, 4001) for category in "xmas"}
        return count_combinations('in', values_intervals)
