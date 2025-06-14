# Copyright 2025 Quantinuum (www.quantinuum.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import stim


class Code6:
    def __init__(self, start, p2=0, m=0):
        # We create a codeblock on six qubits, starting at start in an ordered array
        qubits = []
        for i in range(0,6):
            qubits.append(start+i)
        self.qubits = qubits
        self.p2 = p2
        self.m = m
    def hadamard(self):
        '''Returns a circuit which does a hadamard on the codeblock'''
        c = stim.Circuit()
        c.append("H", self.qubits)
        return c
    def s_dag(self):
        '''Returns a circuit which does a phase dagger gate on the codeblock'''
        c = stim.Circuit()
        c.append("S_DAG", self.qubits)
        return c

    def s(self):
        '''Returns a circuit which does a phase gate on the codeblock'''
        c = stim.Circuit()
        c.append("S", self.qubits)
        return c
    def cnot(self, b2):
        '''Returns a circuit which does a CNOT between two codeblocks'''
        c = stim.Circuit()
        for i in range(0,6):
            c.append("CNOT", [self.qubits[i],b2.qubits[i]])
            c.append("Depolarize2", [self.qubits[i], b2.qubits[i]], self.p2)
        return c
        
    def cz(self, b2):
        '''Returns a circuit which does a CZ between two codeblocks'''
        c = stim.Circuit()
        for i in range(0,6):
            c.append("CZ", [self.qubits[i],b2.qubits[i]])
            c.append("Depolarize2", [self.qubits[i], b2.qubits[i]], self.p2)
        return c
    def cy(self, b2):
        '''Returns a circuit which does a controlled-Y between two codeblocks'''
        c = stim.Circuit()
        for i in range(0,6):
            c.append("CY", [self.qubits[i],b2.qubits[i]])
            c.append("Depolarize2", [self.qubits[i], b2.qubits[i]], self.p2)
        return c


    def x(self):
        '''Returns a circuit which does an X on the codeblock'''
        c = stim.Circuit()
        c.append("X", self.qubits)
        return c
    def measure(self):
        '''returns a circuit which measures all 6 qubits'''
        c = stim.Circuit()
        c.append("MR", self.qubits, self.p2)
        return(c)
    def rypi2(self, b1):
        '''given an ancilla codeblock initialized to the + state, performs a -pi/2 y rotation on self, modulo a y correction'''
        c = stim.Circuit()
        c += b1.cy(self)
        c += b1.s_dag()
        c += b1.hadamard()
        c += b1.measure()
        return c



def get_logicals(list):
    '''given a list of 6 numbers, it returns the value of logical Z0 = Z0Z2Z4 and logical Z1 = Z1Z3Z5'''
    z0 = 0
    z1 = 0
    for i in range(0,3):
        z0 += list[2*i]
        z1 += list[2*i + 1]
    z0 = z0%2
    z1 = z1%2
    return([z0,z1])
def get_stabs(list):
    '''given a list of 6 numbers, returns the 2 stabilizer values of the [[6,2,2]] code'''
    return([(list[0] + list[1] + list[2] + list[3])%2, (list[2] + list[3] + list[4] + list[5])%2])


def get_dist_circ(start, aux, p=0, m=0):
    '''Distills a [[6,2,2]] H state'''
    c = stim.Circuit()
    c.append("H", [start,start+1]) #The magic state we are distilling/encoding
    c.append("H", [start+2,start + 4])
    c.append("CX", [start+2,start + 3])
    c.append("Depolarize2", [start+2,start + 3], p)
    c.append("CX", [start + 4,start + 5])
    c.append("Depolarize2", [start + 4,start + 5], p)
    c.append("Depolarize1", [start,start+1], m)
    
    c.append("CX", [start+2,start])
    c.append("Depolarize2", [start+2,start], p)
    c.append("CX", [start + 3,start+1])
    c.append("Depolarize2", [start + 3,start+1], p)
    c.append("Depolarize1", [start + 4,start + 5], m)

    
    c.append("CX", [start,start + 4])
    c.append("Depolarize2", [start,start + 4], p)
    c.append("CX", [start+1,start + 5])
    c.append("Depolarize2", [start+1,start + 5], p)
    c.append("Depolarize1", [start+2,start + 3], m)

    
    c.append("CX", [start + 4,start+2])
    c.append("Depolarize2", [start + 4,start+2], p)
    c.append("CX", [start + 5,start + 3])
    c.append("Depolarize2", [start + 5,start + 3], p)
    c.append("Depolarize1", [start,start+1], m)
    
    c.append("H", [aux]) #Creating the bell-pair ancilla
    c.append("CX", [aux,aux+1])
    c.append("Depolarize2", [aux, aux+1], p)
    
    c.append("CX", [aux,start])
    c.append("Depolarize2", [aux, start], p)
    c.append("CX", [aux+1,start+1])
    c.append("Depolarize2", [aux+1, start+1], p)
    c.append("Depolarize1", [start+2,start + 3,start + 4,start + 5], m)
    
    c.append("CX", [aux,start+2])
    c.append("Depolarize2", [aux, start+2], p)
    c.append("CX", [aux+1,start + 3])
    c.append("Depolarize2", [aux+1, start + 3], p)
    c.append("Depolarize1", [start,1,start + 4,start + 5], m)



    
    c.append("CX", [aux,start + 4])
    c.append("Depolarize2", [aux, start + 4], p)
    c.append("CX", [aux+1,start + 5])
    c.append("Depolarize2", [aux+1, start + 5], p)
    c.append("Depolarize1", [start+2,start + 3,start,start+1], m)
    
    
    c.append("CX", [aux,aux+1])
    c.append("Depolarize2", [aux, aux+1], p)
    
    c.append("H", [aux])
    c.append("MR", [aux,aux+1], p)
    c.append("Depolarize1", [start,start+1,start+2,start + 3,start + 4,start + 5], m)

    return c

def get_init_circ(start, anc, p, m):
    '''returns fault-tolerant initialization circuit on qubits beginning at index start. Using two ancillas at index anc'''
    c = stim.Circuit()
    c.append("H", [start, start+2])
    c.append("CNOT", [start, anc])
    c.append("Depolarize2", [start, anc], p)
    c.append("CNOT", [start+2, anc+1])
    c.append("Depolarize2", [start+2,anc+1], p)
    
    c.append("CNOT", [start, start+1])
    c.append("Depolarize2", [start,start+1], p)
    c.append("CNOT", [start+2, start+3])
    c.append("Depolarize2", [start+2,start+3], p)

    #Now we noiselessly initialize the other qubits in the codeblock and they start accumulating memory error
    
    c.append("CNOT", [start, start + 4])
    c.append("Depolarize2", [start,start+4], p)
    c.append("CNOT", [start+2, start+5])
    c.append("Depolarize2", [start+2,start+5], p)
    c.append("Depolarize1", [start+1, start+3, anc, anc+1], m)
    

    
    c.append("CNOT", [start, start + 5])
    c.append("Depolarize2", [start,start+5], p)
    c.append("CNOT", [start+2, start+4])
    c.append("Depolarize2", [start+2,start+4], p)
    c.append("Depolarize1", [start+1,start+3, anc, anc+1], m)

    
    c.append("CNOT", [start, anc])
    c.append("Depolarize2", [start, anc], p)
    c.append("CNOT", [start+2, anc+1])
    c.append("Depolarize2", [start+2,anc+1], p)
    c.append("Depolarize1", [start+1,start + 3,start + 4,start + 5], m)

    
    c.append("MR", [anc, anc+1], p)
    #c.append("MR", [start,start+1,start+2,start+3,start+4,start+5], p)
    return(c)