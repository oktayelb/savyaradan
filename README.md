# savyaradanadan: Turkish Morphological Analyzer & Generator

savyaradanadan is a robust, rule-based computational linguistics engine designed for the Turkish language. It provides a complete pipeline to programmatically decompose complex Turkish words into all grammatically legal root-suffix chains, as well as generate valid word forms from base roots.

## Key Features

* **Comprehensive Decomposition:** Finds every possible valid root and suffix combination for a given word using a rigorous depth-first search (DFS) algorithm.
* **Agglutinative Generation:** Generates valid Turkish words from a bare root using breadth-first search (BFS), adhering strictly to Turkish morphology rules.
* **Advanced Phonological Processing:** Automatically applies complex Turkish phonology rules on the fly, including:
  * Major (2-way) and Minor (4-way) Vowel Harmony.
  * Consonant Hardening (Fıstıkçı Şahap).
  * Consonant Softening (e.g., *k* -> *ğ*).
  * Vowel Drop and Collision Buffering (e.g., inserting *y* or *n*).
  * Consonant Gemination Reversal (e.g., *hakk* -> *hak*).
* **Strict Suffix Hierarchy:** Implements a state machine utilizing a waterfall hierarchy (`SuffixGroup`) to ensure suffixes only attach in grammatically legal sequences, with built-in handlers for exceptions like derivational resets and the *-ki* relativizer.
* **Reduplication (Pekiştirme):** Native support for generating and analyzing intensified adjectives and adverbs (e.g., *masmavi*, *güpegündüz*).
* **High Performance Optimization:** Features an optional first-character dispatch index (`SuffixIndex`) and extensive cross-root shared caching and LRU memoization to drastically accelerate processing speeds over large corpora.
* **Closed-Class Word Support:** Identifies and tags function words (pronouns, conjunctions, postpositions) alongside open-class roots.

## Project Structure

```text
savyaradan/
├── main.py                  # CLI entry point and generation logic (savyaradan)
├── data/
│   └── words.txt            # Base dictionary of Turkish lemmas
└── util/                    # Core rule-based morphological engine
    ├── decomposer.py        # Main engine for decomposing words into suffix chains
    ├── suffix.py            # Base classes defining suffix behaviors and hierarchies
    ├── suffix_index.py      # Pre-computed acceleration index for rapid lookup
    ├── word_methods.py      # Dictionary state, root generation, and phonology utilities
    ├── suffixes/            # Suffix definitions categorized by POS transition (n2n, n2v, etc.)
    └── words/               # Closed-class word definitions
