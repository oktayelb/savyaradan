from typing import List, Set, Tuple
from util.suffix import Type, HasMajorHarmony
import util.word_methods as wrd
from util.decomposer import SUFFIX_TRANSITIONS, is_valid_transition, get_pekistirme_analyses

# --- Module Level Helper Functions ---

def apply_bidirectional_harmony(word: str, suffix_text: str) -> str:
    """
    Applies major vowel harmony in both directions (Back->Front and Front->Back)
    using util.word_methods logic.
    """
    if not suffix_text:
        return suffix_text

    harmony = wrd.major_harmony(word) #
    chars = list(suffix_text)
    new_chars = []

    # Mapping logic using word_methods constants
    for char in chars:
        if harmony == wrd.MajorHarmony.FRONT:
            # Force Back vowels to Front
            if char == 'a': char = 'e'
            elif char == 'ı': char = 'i'
            elif char == 'u': char = 'ü'
            elif char == 'o': char = 'ö'
        elif harmony == wrd.MajorHarmony.BACK:
            # Force Front vowels to Back
            if char == 'e': char = 'a'
            elif char == 'i': char = 'ı'
            elif char == 'ü': char = 'u'
            elif char == 'ö': char = 'o'
        new_chars.append(char)
    
    return "".join(new_chars)

def generate_pekistirme_candidates(root: str) -> List[str]:
    """
    Generates potential pekiştirme candidates (e.g. masmavi) and validates them
    using the existing 'get_pekistirme_analyses' in decomposer.py.
    """
    # 1. Find first vowel for prefix generation
    first_vowel_idx = -1
    for i, char in enumerate(root):
        if char in wrd.VOWELS: #
            first_vowel_idx = i
            break
    
    if first_vowel_idx == -1: 
        return []

    prefix_base = root[:first_vowel_idx + 1] # e.g. "ma" from "mavi"
    candidates = []
    valid_results = []

    # 2. Generate raw candidates (m, p, r, s rules)
    consonants = ['m', 'p', 'r', 's']
    
    # Form 1: Standard (ma-s-mavi)
    for c in consonants:
        candidates.append(prefix_base + c + root)
        
    # Form 2: With connecting vowel (gü-p-e-gündüz)
    for c in consonants:
        for v in ['a', 'e']:
            candidates.append(prefix_base + c + v + root)

    # 3. Validate using decomposer logic
    for cand in candidates:
        # get_pekistirme_analyses returns a list of tuples: (root, pos, chain, final_pos)
        analyses = get_pekistirme_analyses(cand) #
        
        # Check if any analysis points back to our original root
        for analysis in analyses:
            found_root = analysis[0]
            if found_root == root:
                valid_results.append(cand)
                break
                
    return valid_results

def should_process_state(state_key: Tuple, visited: Set) -> bool:
    """Checks if the state has been visited."""
    if state_key in visited:
        return False
    visited.add(state_key)
    return True

def should_add_to_results(target_pos_filter: str, current_pos: str) -> bool:
    """Determines if the current word matches the requested POS filter."""
    if not target_pos_filter:
        return True
    
    is_verb = (current_pos == 'verb')
    if target_pos_filter == 'verb' and not is_verb: return False
    if target_pos_filter == 'noun' and is_verb: return False
    
    return True

# --- Main Logic ---

def savyaradan(
    root: str, 
    max_suffix_count: int = 3, 
    allowed_max_group: int = 15,
    target_pos: str = None
) -> List[str]:
    """
    Generates valid Turkish words from a root using BFS traversal of suffix transitions.
    """
    
    # 1. Initialize Queue
    queue = []
    if wrd.can_be_noun(root): #
        queue.append((root, 'noun', []))
    if wrd.can_be_verb(root): #
        queue.append((root, 'verb', []))
        
    generated_words = set()
    visited_states = set() # Stores (text, pos)

    while queue:
        current_text, current_pos, chain = queue.pop(0)

        # --- Visited Check (Must be before processing) ---
        state_key = (current_text, current_pos)
        if not should_process_state(state_key, visited_states):
            continue
        
        # --- Add to Results ---
        # Add if we have applied at least one suffix (or pekiştirme logic)
        # OR if we want to include the root itself (optional, usually generator implies derivatives)
        if chain: 
            if should_add_to_results(target_pos, current_pos):
                # Format: "gel-" for verbs, "ev" for nouns
                display_text = current_text + ("-" if current_pos == 'verb' else "")
                generated_words.add(display_text)
        
        if len(chain) >= max_suffix_count:
            continue

        # 2. Get Candidates
        possible_transitions = SUFFIX_TRANSITIONS.get(current_pos, {}) #
        
        for target_pos_key, suffix_list in possible_transitions.items():
            for suffix in suffix_list:
                
                # --- Filter: Hierarchy & Constraints ---
                if suffix.group > allowed_max_group: continue
                if suffix.comes_to == Type.NOUN and current_pos != 'noun': continue
                if suffix.comes_to == Type.VERB and current_pos != 'verb': continue
                
                if chain:
                    if not is_valid_transition(chain[-1], suffix): continue #
                
                if suffix.is_unique and any(s.name == suffix.name for s in chain):
                    continue

                # --- Special Case: Pekiştirme ---
                if suffix.name == "pekistirme":
                    # Only apply pekiştirme to bare roots (chain is empty)
                    if not chain:
                        valid_pekistirmes = generate_pekistirme_candidates(current_text)
                        for p_word in valid_pekistirmes:
                            # Pekiştirme results are Nouns/Adjectives
                            queue.append((p_word, 'noun', chain + [suffix]))
                    continue

                # --- Standard Generation ---
                # Suffix form generation
                raw_forms = suffix.form(current_text) #
                
                for form_part in raw_forms:
                    # Fix Harmony using Utility-based function
                    if suffix.major_harmony == HasMajorHarmony.Yes:
                        final_suffix_part = apply_bidirectional_harmony(current_text, form_part)
                    else:
                        final_suffix_part = form_part

                    new_word = current_text + final_suffix_part
                    new_chain = chain + [suffix]
                    
                    # Determine Next POS
                    next_pos_candidates = []
                    if suffix.makes == Type.NOUN:
                        next_pos_candidates.append('noun')
                    elif suffix.makes == Type.VERB:
                        next_pos_candidates.append('verb')
                    elif suffix.makes == Type.BOTH:
                        next_pos_candidates.append('noun')
                        next_pos_candidates.append('verb')
                    
                    for next_pos in next_pos_candidates:
                        queue.append((new_word, next_pos, new_chain))

    return sorted(list(generated_words))

if __name__ == "__main__":
    test_root = "mavi"
    while test_root != "":
        test_root = input("kök (çıkış için enter): ")
        if not test_root: break
        
        print(f"\n--- {test_root} için sonuçlar ---")
        results = savyaradan(test_root, max_suffix_count=1)
        for w in results:
            print(w)