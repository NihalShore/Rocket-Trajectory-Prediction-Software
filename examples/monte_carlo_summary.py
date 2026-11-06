"""Summarize a seeded parameter sample without hiding its distribution."""
from rocket_sim.uncertainty import sample_normal,summarize
samples=sample_normal(mean=0.0,std=0.03,count=1000,seed=2026)
summary=summarize("fractional thrust variation",samples)
print(summary)
