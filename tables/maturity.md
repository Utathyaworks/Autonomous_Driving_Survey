# Algorithmic maturity by on-road entropy

M1 mature and fielded; M2 proven, not deployed at that complexity; M3 research prototype; M4 absent. E1 to E5 grade the road, from segregated motorway to lane-free negotiated flow.

## Sense

| Method family | E1 | E2 | E3 | E4 | E5 | Basis of the hardest grade |
|---|---|---|---|---|---|---|
| Camera detection & segmentation | M1 | M1 | M2 | M3 | M4 | Large measured accuracy fall on unstructured roads |
| LiDAR 3D detection | M1 | M1 | M2 | M3 | M4 | Trained on closed vocabularies without small mixed agents |
| Camera-only BEV detection | M1 | M2 | M3 | M3 | M4 | Depth lifting degrades where scale priors fail |
| Camera-LiDAR BEV fusion | M1 | M1 | M2 | M3 | M4 | Fusion weighting never trained to arbitrate dense mixed traffic |
| Radar-camera fusion | M2 | M2 | M3 | M3 | M4 | Weather-robust but data-starved; sparsity and ghost targets |
| Occupancy prediction | M2 | M2 | M3 | M3 | M4 | Open-set by design, but evaluated only on structured scenes |
| Multi-object tracking | M1 | M1 | M2 | M3 | M4 | Association assumes separable, non-filtering agents |
| Adverse-condition robustness | M1 | M2 | M2 | M3 | M4 | Adverse \times unstructured has no public benchmark |
| Event and thermal sensing | M2 | M3 | M3 | M3 | M4 | Annotation scarcity, not physics, is the binding limit |
| Cooperative V2X perception | M2 | M2 | M3 | M4 | M4 | Requires roadside infrastructure absent in E4/E5 jurisdictions |
| Online calibration & sensor health | M1 | M1 | M2 | M3 | M4 | Vibration, dust and no recalibration service network |
| Real-time / streaming perception | M1 | M1 | M2 | M3 | M4 | Compute envelope of E4/E5 vehicle classes is far smaller |

## Plan

| Method family | E1 | E2 | E3 | E4 | E5 | Basis of the hardest grade |
|---|---|---|---|---|---|---|
| Search, sampling and lattice planning | M1 | M1 | M2 | M3 | M4 | Lane-free by construction but demonstrated only at low speed in car-park-like zones |
| Frenet-frame trajectory generation | M1 | M1 | M2 | M4 | M4 | The frame is defined relative to a centreline; without one the representation does not exist |
| Optimisation-based local planning | M1 | M1 | M2 | M3 | M4 | Requires a drivable corridor and a homotopy class chosen outside the optimiser |
| Imitation and end-to-end planning | M2 | M2 | M3 | M3 | M4 | Deployed only under human supervision; open-loop scores do not predict closed-loop quality |
| Physics-based short-horizon prediction | M1 | M1 | M1 | M2 | M3 | Entropy-independent, but its useful horizon of about 1 s is far shorter than the interaction horizon at E4/E5 |
| Deep multi-modal, joint and occupancy forecasting | M2 | M2 | M3 | M3 | M4 | Escapes fixed agent count and detection dependence, but trained and scored only on structured logs |
| Map-conditioned forecasting | M2 | M2 | M3 | M4 | M4 | The lane graph is the principal input; removing it removes the model's strongest feature |
| Pedestrian and cyclist intention | M2 | M2 | M3 | M3 | M4 | E4 annotations now exist but no fielded or independent evaluation follows them |
| Routing and route-graph search | M1 | M1 | M1 | M1 | M2 | Solved wherever a digital road graph exists; informal streets are absent or misrepresented in the graph |
| HD mapping, online mapping and map-relative pose | M1 | M1 | M2 | M4 | M4 | The lane-centreline schema is undefined where lateral position is continuous, and online mapping predicts only the marked-lane vocabulary it was trained on |
| Interaction-aware decision making | M2 | M2 | M3 | M3 | M4 | Tractability rests on a small discrete policy set that presumes lane semantics |
| Deadlock detection and resolution | M2 | M2 | M3 | M4 | M4 | Fielded resolution escalates to a remote human; formal guarantees require centralisation |
| Safety metrics, formal models and evaluation protocols | M1 | M2 | M2 | M4 | M4 | Metrics disagree and several are undefined in crossing and lane-free geometries; no E4 scenario catalogue exists |
| Takeover, monitoring and external HMI | M1 | M2 | M2 | M3 | M4 | Codified only for motorway operation; implicit negotiation is in no deployed planner |

## Act

| Method family | E1 | E2 | E3 | E4 | E5 | Basis of the hardest grade |
|---|---|---|---|---|---|---|
| Geometric path tracking | M1 | M1 | M1 | M2 | M3 | Proven on an unpaved desert course, but without traffic and at low speed |
| Dynamic-model lateral control | M1 | M1 | M2 | M3 | M4 | Linear-tyre region invalid and unobservable on loose or damaged surfaces |
| PID longitudinal control & ACC | M1 | M1 | M1 | M2 | M3 | Gap regulation presumes one identifiable in-lane lead vehicle |
| Model predictive control | M1 | M1 | M2 | M3 | M4 | Constraints presume known friction and modelled agent futures |
| Robust & learning-based MPC | M2 | M2 | M3 | M3 | M4 | Demonstrated on test tracks and in racing; no public-road deployment |
| By-wire actuation, four-wheeler | M1 | M1 | M1 | M1 | M1 | Physically indifferent to road entropy; type-approved and fielded |
| By-wire actuation, two-/three-wheeler | M2 | M2 | M3 | M4 | M4 | Braking and traction intervention only; no steering or trajectory authority exists as a product |
| Fail-operational architecture | M1 | M1 | M2 | M3 | M4 | Certified only inside mapped motorway or geofenced domains |
| Minimal risk manoeuvre & fallback | M1 | M1 | M2 | M4 | M4 | No definition of a safe stopping state on a lane-free carriageway |
| Deep RL for vehicle control | M2 | M3 | M3 | M4 | M4 | One real-vehicle demonstration on a private road; no simulator reproduces mixed unstructured flow |
| Imitation & offline RL policies | M2 | M2 | M3 | M3 | M4 | Closed-loop evaluation confined to logged structured traffic |
| Runtime assurance & safety filters | M2 | M2 | M3 | M4 | M4 | Every method needs a codified rule set; E4/E5 conventions are unwritten |
