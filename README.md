

# Savyaradan: Türkçe Morfolojik Kelime Üretici

Savyaradan, verilen bir kök kelimeye sistematik olarak ek zincirleri uygulayarak dilbilgisi kurallarına uygun Türkçe kelimeler üreten Python tabanlı bir morfoloji motorudur.

###  Nasıl Çalışır?
Motor, geçerli ek geçişlerinden oluşan bir ağacı taramak için **Sığ Öncelikli Arama (Breadth-First Search - BFS)** algoritmasını kullanır. Kök kelimenin isim veya fiil olma durumuna göre, belirlenen bir derinliğe (`max_suffix_count`) kadar olası kombinasyonları araştırır ve bu süreçte katı dilbilgisi kurallarını uygular.

###  Temel Özellikler
* **Akıllı Tarama (BFS):** Sonsuz döngüleri önlemek için ziyaret edilen durumları (visited-states) takip ederek tüm geçerli morfolojik olasılıkları tarar.
* **Çift Yönlü Büyük Ünlü Uyumu:** Eklerdeki ünlü harfleri kök kelimeye uyum sağlayacak şekilde otomatik olarak (Kalın ↔ İnce) dönüştüren dinamik bir Büyük Ünlü Uyumu sistemi içerir.
* **Pekiştirme Motoru:** Ünsüz türeme kurallarını (m, p, r, s) kullanarak pekiştirmeli sıfatları (örn. *mavi* -> *masmavi*, *gündüz* -> *güpegündüz*) otomatik olarak üretir ve doğrular.
* **Kelime Türü (POS) Takibi:** Kelimelerin İsim ve Fiil formları arasındaki geçişlerini dinamik olarak izler ve eklerin yalnızca geçerli dilbilgisi durumlarına uygulanmasını sağlar.
* **Hiyerarşik Filtreleme:** Ek gruplandırmalarına ve geçiş kurallarına uyar, benzersiz (unique) eklerin tekrar tekrar eklenmesini engeller.

###  Bilinen Sorunlar ve Kısıtlamalar
* **Yapım Eki ve Çekim Eki Ayrımı:** Mevcut durumda motor, yapım ekleri ile çekim ekleri arasında kusursuz bir ayrım yapmamaktadır. Sadece yeni kelimeler türeten yapım eklerini değil, çekim eklerini de ekleyerek aşırı çekimlenmiş formlar üretebilmektedir.
* **Ek Birleşme Hataları:** Bazı eklerin köke veya birbirine bağlanması sırasında, daha sıkı geçiş kısıtlamaları gerektiren uygulama sorunları bulunmaktadır.

###  Kullanım
İnteraktif arayüzü başlatmak için betiği çalıştırın:
`python main.py`

Üretilen tüm varyasyonları görmek için bir kök kelime yazın (örn. `mavi` veya `gel`). Çıkmak için boş ekranda `Enter` tuşuna basın.

---

# Savyaradan: Turkish Morphological Generator

Savyaradan is a Python-based morphological engine designed to generate grammatically valid Turkish words by systematically applying suffix chains to a provided root word. 

### How It Works
The engine uses a **Breadth-First Search (BFS)** algorithm to traverse a tree of valid suffix transitions. Depending on whether the root word functions as a noun or a verb, the generator explores possible combinations up to a specified depth (`max_suffix_count`), applying strict grammatical rules along the way.

### Core Features
* **Intelligent Traversal (BFS):** Explores all valid morphological states while using a visited-state tracker to prevent infinite loops.
* **Bi-directional Vowel Harmony:** Implements dynamic Major Vowel Harmony, automatically shifting suffix vowels (Front ↔ Back) to harmonize with the root word.
* **"Pekiştirme" (Intensification) Engine:** Automatically generates and validates intensified adjectives (e.g., *mavi* -> *masmavi*, *gündüz* -> *güpegündüz*) using consonant insertion rules (m, p, r, s).
* **Part-of-Speech (POS) Tracking:** Dynamically tracks word states as they transition between Nouns and Verbs, ensuring suffixes are only applied to valid grammatical states.
* **Hierarchical Filtering:** Respects suffix groupings and transition rules, ensuring unique suffixes aren't applied redundantly.

### Known Issues & Limitations
* **Inflectional vs. Derivational Suffixes:** Currently, the generator does not distinguish perfectly between derivational suffixes (*yapım ekleri*) and inflectional suffixes (*çekim ekleri*). It may append non-derivational suffixes, leading to heavily inflected forms rather than strictly new derived base words.
* **Transition Edge Cases:** There are still occasional issues with certain suffix attachments that require tighter transition constraints.

### Usage
Run the script to enter an interactive prompt:
`python main.py`

Type a root word (e.g., `mavi` or `gel`) to see all generated variations. Press `Enter` on an empty prompt to exit.

