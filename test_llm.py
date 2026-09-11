from llm_extractor import extract_note_with_llm

note = """
SYNTHETIC EXAMPLE ONLY. A 29-year-old woman has papilloedema confirmed by an AO.
Visual function is explicitly documented as not threatened. BP is 130/80.
MRI brain is normal. MRV is normal. FBC is normal. LP was completed and opening
pressure was 31 cm CSF. LP technique was valid. CSF protein, glucose and cells
are available and normal.
"""

result = extract_note_with_llm(note)
print(result)
