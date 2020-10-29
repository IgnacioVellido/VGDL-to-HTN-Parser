;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PDDL problem for a VGDL game
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; w0 w1 w2
; h0 b1 a0
; b0 f8 h2
; f10 f11 f12
; f13 b2 f15
; f16 f17 h1


(define (problem VGDLProblem) (:domain VGDLGame)

	; Objects ---------------------------------------------------------------------

	(:objects
			w0 w1 w2 - wall
			f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 f13 f14 f15 f16 f17 f18 - floor
			a0 - avatar
			b0 b1 b2 - box
			h0 h1 - hole
	)

	; Init -----------------------------------------------------------------

	(:init
			(oriented-right a0)
			(can-move-up a0)
			(can-move-down a0)
			(can-move-left a0)
			(can-move-right a0)

			(at f1 w0)
			(at f2 w1)
			(at f3 w2)
			(at f4 h0)
			(at f5 b1)
			(at f6 a0)
			(at f7 b0)
			(at f14 b2)
			(at f18 h1)
			
			(last-at f1 w0)
			(last-at f2 w1)
			(last-at f3 w2)
			(last-at f4 h0)
			(last-at f5 b1)
			(last-at f6 a0)
			(last-at f7 b0)
			(last-at f14 b2)
			(last-at f18 h1)

			(connected-right f1 f2)
			(connected-right f2 f3)
			(connected-right f4 f5)
			(connected-right f5 f6)
			(connected-right f7 f8)
			(connected-right f8 f9)

			(connected-left f2 f1)
			(connected-left f3 f2)
			(connected-left f5 f4)
			(connected-left f6 f5)
			(connected-left f8 f7)
			(connected-left f9 f8)

			(connected-up f4 f1)
			(connected-up f7 f4)
			(connected-up f5 f2)
			(connected-up f8 f5)
			(connected-up f6 f3)
			(connected-up f9 f6)

			(connected-down f1 f4)
			(connected-down f4 f7)
			(connected-down f2 f5)
			(connected-down f5 f8)
			(connected-down f3 f6)
			(connected-down f6 f9)


			(connected-down f7 f10)
			(connected-down f8 f11)
			(connected-down f9 f12)

			(connected-up f10 f7)
			(connected-up f11 f8)
			(connected-up f12 f9)

			(connected-right f10 f11)
			(connected-left f11 f10)
			(connected-right f11 f12)
			(connected-left f12 f11)


			(connected-down f10 f13)
			(connected-down f11 f14)
			(connected-down f12 f15)

			(connected-up f13 f10)
			(connected-up f14 f11)
			(connected-up f15 f12)

			(connected-right f13 f14)
			(connected-left f14 f13)
			(connected-right f14 f15)
			(connected-left f15 f14)



			(connected-down f13 f16)
			(connected-down f14 f17)
			(connected-down f15 f18)

			(connected-up f16 f13)
			(connected-up f17 f14)
			(connected-up f18 f15)

			(connected-right f16 f17)
			(connected-left f17 f16)
			(connected-right f17 f18)
			(connected-left f18 f17)

			(turn-avatar)
	)

	; Goals -----------------------------------------------------------------

	(:goal
		(and
			; To end in new turn
			; (turn-avatar)
			
			(not (at f1 b1))
			(not (at f2 b1))
			(not (at f3 b1))
			(not (at f4 b1))
			(not (at f5 b1))
			(not (at f6 b1))
			(not (at f7 b1))
			(not (at f8 b1))
			(not (at f9 b1))
			(not (at f10 b1))
			(not (at f11 b1))
			(not (at f12 b1))
			(not (at f13 b1))
			(not (at f14 b1))
			(not (at f15 b1))
			(not (at f16 b1))
			(not (at f17 b1))
			(not (at f18 b1))


			(not (at f1 b0))
			(not (at f2 b0))
			(not (at f3 b0))
			(not (at f4 b0))
			(not (at f5 b0))
			(not (at f6 b0))
			(not (at f7 b0))
			(not (at f8 b0))
			(not (at f9 b0))
			(not (at f10 b0))
			(not (at f11 b0))
			(not (at f12 b0))
			(not (at f13 b0))
			(not (at f14 b0))
			(not (at f15 b0))
			(not (at f16 b0))
			(not (at f17 b0))
			(not (at f18 b0))

			; (not (at f1 b2))
			; (not (at f2 b2))
			; (not (at f3 b2))
			; (not (at f4 b2))
			; (not (at f5 b2))
			; (not (at f6 b2))
			; (not (at f7 b2))
			; (not (at f8 b2))
			; (not (at f9 b2))
			; (not (at f10 b2))
			; (not (at f11 b2))
			; (not (at f12 b2))
			; (not (at f13 b2))
			; (not (at f14 b2))
			; (not (at f15 b2))
			; (not (at f16 b2))
			; (not (at f17 b2))
			; (not (at f18 b2))
		)
	)
)