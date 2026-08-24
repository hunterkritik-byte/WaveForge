# WaveForge feature matrix

WaveForge remains a software-only wireless simulation environment. The following capabilities are modeled locally and do not access or transmit through real wireless interfaces.

## Simulation and physics

1. Node movement
2. Position bounds
3. Euclidean distance
4. Path-loss modeling
5. Received-power modeling
6. RSSI modeling
7. Noise-floor modeling
8. SNR calculation
9. Link-quality normalization
10. Fading/jitter
11. Deterministic noise
12. Channel utilization
13. Channel interference
14. Channel scoring
15. Best-channel selection
16. Channel summaries
17. Collision probability
18. Airtime estimation
19. Capacity estimation
20. Queue-delay estimation

## Packet and transport telemetry

21. Packet traces
22. Packet delivery ratio
23. Packet-loss ratio
24. Retry budgets
25. Latency budgets
26. Throughput calculation
27. Packet-size generation
28. Delivery/drop accounting
29. Retry accounting
30. Mean-latency telemetry
31. Drop counters
32. Run-to-run metric comparison
33. Deterministic run IDs
34. Deterministic event timing
35. SLA checks

## Network behavior

36. Topology-edge generation
37. Seeded node generation
38. Node enable/disable state
39. Battery state
40. Battery consumption
41. Availability scoring
42. Node metadata/tags
43. TX-power modeling
44. Channel state objects
45. Multi-channel summaries

## Analytics

46. Moving averages
47. Exponential smoothing
48. Percentiles
49. Histograms
50. Confidence intervals
51. Weighted scoring
52. Confidence scoring
53. Fairness index
54. Signal normalization
55. MAC normalization
56. Channel validation
57. Run comparison
58. Deterministic random seeds
59. Reproducible packet distributions
60. Reproducible jitter

## Safety boundary

WaveForge does **not** implement wireless packet transmission, deauthentication, jamming, live-interface capture, credential collection, nearby-network scanning, or interference with third-party systems. All features above operate on simulated objects and synthetic data.
