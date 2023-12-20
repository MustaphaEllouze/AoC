from typing import Any
from dataclasses import dataclass
from abc import abstractmethod

from aoc.tools import ABCSolver

@dataclass
class Signal:
    pitch:int
    def __post_init__(self, )->None:
        assert self.pitch in [0,1]
    @property
    def is_low(self,) : return self.pitch==0
    @property
    def is_high(self,) : return self.pitch==1

LOW = Signal(0)
HIGH = Signal(1)

VERBOSE = False

@dataclass
class Station :
    name:str
    children:list['Station'] = None
    parents:list['Station'] = None

    def __post_init__(self,)->None:
        if self.children is None : self.children = []
        if self.parents is None : self.parents = []
        self.received_signal = None
        for c in self.children :
            c.parents.append(self)

    @abstractmethod
    def process_signal(self)->None:
        pass

    def receive_signal(self, signal:Signal, parent:'Station'=None)->None:

        parent_name = 'Button' if parent is None else parent.name
        signal_name = 'LOW' if signal is LOW else 'HIGH'

        if VERBOSE : print(f'{parent_name} sent {signal_name} to {self.name}')
        self.received_signal = signal

    def send_signal(self, signal:Signal)->Signal:
        for c in self.children :
            c.receive_signal(signal, parent=self)

    def reset(self,)->None:
        self.received_signal = None

@dataclass
class FlipFlop(Station):
    state:bool=False

    def process_signal(self) -> Signal:
        send_this = None
        if self.received_signal is HIGH : pass
        else :
            self.state = not self.state
            if self.state :
                send_this = HIGH
            else:
                send_this = LOW
            # self.send_signal(send_this)
        self.reset()
        return send_this


@dataclass
class Broadcaster(Station):
    def process_signal(self) -> Signal:
        received = self.received_signal
        # self.send_signal(received)
        self.reset()
        return received

@dataclass
class Conjugater(Station):

    def __post_init__(self) -> None:
        super().__post_init__()
        self.remembered = {p.name:LOW for p in self.parents}

    def initialize_conjugater(self)->None:
        self.remembered = {p.name:LOW for p in self.parents}


    def receive_signal(self, signal: Signal, parent: 'Station' = None) -> None:
        super().receive_signal(signal, parent)
        assert parent is not None
        self.remembered[parent.name] = signal

    def process_signal(self) -> Signal:
        signal = None
        if all([s is HIGH for s in self.remembered.values()]):
            # self.send_signal(LOW)
            signal = LOW
        else:
            # self.send_signal(HIGH)
            signal = HIGH
        self.reset()
        return signal


@dataclass
class Network:
    broadcaster:Broadcaster
    flip_flops:dict[str, FlipFlop]
    conjugaters:dict[str, FlipFlop]

    def push_button(self, part2:bool=False, va_part2:int=0, station_name:str='')->tuple[int, int]:
        # self.broadcaster.receive_signal(signal=LOW)
        nb_low_pulse = 0
        nb_high_pulse = 0

        to_be_processed = [(self.broadcaster, LOW, None)]
        while to_be_processed :
            # print([e[0].name for e in to_be_processed])

            station, signal, parent = to_be_processed.pop(0)

            if part2:
                if parent is not None and parent.name == station_name and signal is HIGH: return va_part2

            if signal is LOW :
                nb_low_pulse += 1
            if signal is HIGH :
                nb_high_pulse += 1

            if signal is None : continue
            else :
                assert parent is not None or station is self.broadcaster
                station.receive_signal(signal=signal, parent=parent)

            sent_signal = station.process_signal()

            for c in station.children :
                to_be_processed.append(
                    (c, sent_signal, station)
                )

        return nb_low_pulse, nb_high_pulse

    @classmethod
    def from_input(cls, input:list[str]):

        broadcaster = Broadcaster('broadcaster', [], [])
        str_broadcaster = [line for line in input if 'broadcaster' in line][0]

        str_stations = [line for line in input if line is not str_broadcaster]
        str_flip = [line for line in str_stations if line[0]=='%']
        str_conj = [line for line in str_stations if line[0]=='&']

        conjugaters = {
            line.split('->')[0][1:].strip() :
            Conjugater(line.split('->')[0][1:].strip(), [], [])
            for line in str_conj
        }

        flip_flops = {
            line.split('->')[0][1:].strip() :
            FlipFlop(line.split('->')[0][1:].strip(), [], [])
            for line in str_flip
        }

        all_active_stations = {}
        all_active_stations.update(conjugaters)
        all_active_stations.update(flip_flops)

        broadcaster.parents = []
        broadcaster.children = [
            all_active_stations.get(e.strip(), None)
            for e in str_broadcaster.split('->')[1].split(',')
        ]

        for c in broadcaster.children : c.parents.append(broadcaster)

        for sf in str_flip+str_conj :
            name_sf = sf.split('->')[0][1:].strip()
            stations = [e.strip() for e in sf.split('->')[1][1:].split(',')]
            flipper = flip_flops.get(name_sf, None) if name_sf in flip_flops else conjugaters.get(name_sf, None)
            flipper.children = [
                all_active_stations.get(e, None)
                if e in all_active_stations.keys()
                else Station(e, children=[], parents=[flipper])
                for e in stations
            ]
            for c in flipper.children :
                c.parents.append(flipper)

        for c in conjugaters.values() : c.initialize_conjugater()
        return Network(
            broadcaster=broadcaster,
            flip_flops=flip_flops,
            conjugaters=conjugaters,
        )

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        network = Network.from_input(self.data)

        nb_push = 1000
        low, high = 0,0
        for i in range(nb_push):
            _low, _high = network.push_button()
            low += _low
            high += _high

        if not part2 : 
            return 'No solution', low*high

        else :

            all_stations = {}
            all_stations.update(network.conjugaters)
            all_stations.update(network.flip_flops)

            # Find parents of rx
            parents_rx = [
                s
                for n,s in all_stations.items()
                if 'rx' in [c.name for c in s.children]
            ]

            if len(parents_rx) == 1 :
                father_rx = parents_rx[0]
                grand_parents_rx= [
                    s
                    for n,s in all_stations.items()
                    if father_rx.name in [c.name for c in s.children]
                ]
                compute_these = grand_parents_rx
            else:
                compute_these = parents_rx

            result_rx = 1

            for father in compute_these :
                network_part2 = Network.from_input(self.data)
                result_father = 1
                while not isinstance(network_part2.push_button(
                    part2=True,
                    va_part2=result_father+1,
                    station_name=father.name
                ), int):
                    result_father += 1
                result_rx *= result_father
            return 'No solution', result_rx
        return super().solve(part2)
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)

