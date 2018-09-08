"""
Bed counter-factual Simulation

Covers:

- Resources: Resource
- Resources: Container
- Waiting for other processes

Scenario:
    We are trying to assess if using a non-greedy approach would
     reduce the number of patients boarded to the wrong ward

- A patient arrives at the ICU - the logic!
beds = simulated_beds + beds_left

# If there are no beds in the correct specialty area irl
if beds_left=0:
    boarded = True
else:
    boarded = False
# If there are no beds in the simulation for the correct specialty area
if beds > 0 | predicted_board:
    simulation_boarded = True
else:
    simulation_boarded = False

if simulation_boarded & boarded:
    wait for a bit
    leave
if simulation_boarded & not boarded:
    increment simulated beds
    wait for a bit
    leave
if not simulation_boarded & boarded:
    decrement simulation beds
    wait for a bit
if not simulation_boarded & not boarded:
    wait for a bit
    leave
"""
import itertools
import random

import simpy


RANDOM_SEED = 42
NUMBER_OF_BEDS = 1000
T_INTER = [30, 300]        # Create a patient every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds

patients = [{'name': 1, 'length_of_stay': 5, 'boarded': 'home', 'predicted_board': True}]


global simulated_beds


def patient(env, name, length_of_stay, boarded):

    print('%s arriving at gas station at %.1f' % (name, env.now))
    with boarded.request() as req:
        start = env.now
        # Request one of the gas pumps
        yield req

        # Stay in a bed for a bit
        yield env.timeout(length_of_stay)

        print('%s left ward in %.1f seconds.' % (name, env.now - start))


def patient_generator(env, patients):
    """Generate new patient that arrive at the ICU."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        p = random.sample(patients, 1)
        print_name = 'Simulation id %d, Data id  %d' % i, p['name']
        env.process(patient(print_name, p['length_of_stay'], p['boarded']))


# Create environment and start processes
env = simpy.Environment()
boarded = simpy.Resource(env, 1)
bed = simpy.Container(env, NUMBER_OF_BEDS, init=NUMBER_OF_BEDS)
env.process(patient_generator(env, patients))

# Execute!
env.run(until=SIM_TIME)


