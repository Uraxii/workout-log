# PAR-Q+ general health questions, verbatim

Source: research/07-baselining-and-assessment.md s1.1, quoting the PAR-Q+ form
dated 01-11-2024, copyright 2025 PAR-Q+ Collaboration
(https://eparmedx.com/wp-content/uploads/2025/01/PARQPlus2025Fillable.pdf).
Instrument citation: Warburton DER, Jamnik VK, Bredin SSD, Gledhill N. Health &
Fitness Journal of Canada 4(2):3-23, 2011.

Licence term, quoted: "You are encouraged to photocopy the PAR-Q+. You must use
the entire questionnaire and NO changes are permitted." `screen` presents all
seven in this exact wording, in this order, and never paraphrases or skips one.

1. "Has your doctor ever said that you have a heart condition OR high blood pressure?"
2. "Do you feel pain in your chest at rest, during your daily activities of living, OR when you do physical activity?"
3. "Do you lose balance because of dizziness OR have you lost consciousness in the last 12 months? Please answer NO if your dizziness was associated with over-breathing (including during vigorous exercise)."
4. "Have you ever been diagnosed with another chronic medical condition (other than heart disease or high blood pressure)?"
5. "Are you currently taking prescribed medications for a chronic medical condition?"
6. "Do you currently have (or have had within the past 12 months) a bone, joint, or soft tissue (muscle, ligament, or tendon) problem that could be made worse by becoming more physically active? Please answer NO if you had a problem in the past, but it does not limit your current ability to be physically active."
7. "Has your doctor ever said that you should only do medically supervised physical activity?"

## Follow-up, on any YES (build-plan s6.1, s6)

`screen` asks one follow-up line per YES: name the condition, and say whether a
clinician has already cleared exercise, with a date. `screen` is the only skill
that writes `config/limits.clearance = "cleared"` off a clinician's own
clearance (rule S8); intake's PAR-Q+ pass never writes that value itself.

- All seven NO: `clearance = cleared`, `parq_date` = today. The form's own text:
  "you are cleared for physical activity... start slowly and build up
  gradually."
- Any YES, clinician clearance given (name + date): `clearance = cleared`.
- Any YES, no clinician clearance yet: `clearance = referred`. The form's own
  text: "you should seek further information before becoming more physically
  active... visit a qualified exercise professional."

## Expiry

The form's participant declaration: clearance "is valid for a maximum of 12
months from the date it is completed and becomes invalid if my condition
changes." `screen` re-fires on either trigger (build-plan s6).
