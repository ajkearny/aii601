(define
(domain space)
(:requirements :strips :typing :action-costs)
(:types location locatable - object
	ship supply - locatable
	plasmaconduit plasmainjector warpcoil dilithium medicalsupply - supply)

(:predicates
  (at ?l - locatable ?p - location)
  (adjacent ?a - location ?b - location)
  (on-ship ?p - supply ?s - ship)
  (warp-enabled ?s - ship)
  )

(:functions
  (distance ?a - location ?b - location)
  (total-cost)
  (warp-distance ?a - location ?b - location)
)

(:action travel-impulse-speed
  :parameters (?s - ship ?from - location ?to - location)
  :precondition (and
    (at ?s ?from)
    (adjacent ?from ?to))
  :effect (and
    (not (at ?s ?from))
    (at ?s ?to)
    (increase (total-cost) (distance ?from ?to))
    ))

(:action enable-warp-drive
  :parameters (?s - ship ?pc - plasmaconduit ?pi - plasmainjector 
  ?wc - warpcoil ?di - dilithium)
  :precondition (and
    (on-ship ?pc ?s)
    (on-ship ?pi ?s)
    (on-ship ?wc ?s)
    (on-ship ?di ?s))
  :effect (and
    (warp-enabled ?s)
    (increase (total-cost) 3)
    ))

(:action travel-warp-speed
  :parameters (?s - ship ?from - location ?to - location)
  :precondition (and
    (at ?s ?from)
    (adjacent ?from ?to)
    (warp-enabled ?s))
  :effect (and
    (not (at ?s ?from))
    (at ?s ?to)
    (increase (total-cost) (warp-distance ?from ?to))
    ))

(:action beam-up-supplies
  :parameters (?s - ship ?l - location ?p - supply)
  :precondition (and
    (at ?s ?l)
    (at ?p ?l))
  :effect (and
    (on-ship ?p ?s)
    (not (at ?p ?l))
    (increase (total-cost) 1)
    ))
)
