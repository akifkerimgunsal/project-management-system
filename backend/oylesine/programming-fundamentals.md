# Temel Programlama ve Algoritmalar
## Kapsamlı Eğitim Dokümanı

### İçindekiler
1. [Algoritma Temelleri](#1-algoritma-temelleri)
2. [Veri Tipleri ve Değişkenler](#2-veri-tipleri-ve-değişkenler)
3. [Kontrol Yapıları](#3-kontrol-yapıları)
4. [Fonksiyonlar/Metotlar](#4-fonksiyonlarmetotlar)
5. [Diziler ve Koleksiyonlar](#5-diziler-ve-koleksiyonlar)
6. [Temel Algoritmalar](#6-temel-algoritmalar)
7. [Nesne Yönelimli Programlama](#7-nesne-yönelimli-programlama)
8. [Hata Yakalama](#8-hata-yakalama)
9. [Temel Veri Yapıları](#9-temel-veri-yapıları)
10. [Dosya İşlemleri](#10-dosya-işlemleri)

## 1. Algoritma Temelleri

### Algoritma Nedir?
Bir problemi çözmek için takip edilmesi gereken adım adım talimatlar bütünüdür. Belirli bir başlangıç durumundan başlayıp, belirli bir sonuca ulaşmak için gerekli adımların tümüdür.

### Algoritmanın Temel Özellikleri
- **Kesinlik:** Her adım açık ve net olmalı
- **Sonluluk:** Algoritma sonlu sayıda adımdan oluşmalı
- **Girdiler:** Sıfır veya daha fazla girdi alabilir
- **Çıktılar:** En az bir çıktı üretmeli
- **Uygulanabilirlik:** Her adım uygulanabilir olmalı

### Algoritma Gösterim Şekilleri
1. **Düz Metin:** Doğal dille yazılan algoritma
2. **Akış Şeması:** Şekillerle gösterilen algoritma
   - Oval: Başla/Bitir
   - Paralelkenar: Giriş/Çıkış
   - Dikdörtgen: İşlem
   - Eşkenar dörtgen: Karar
3. **Sözde Kod (Pseudocode):** Programlama diline benzer ama serbest yapıda yazım

### Algoritma Analizi
- **Zaman Karmaşıklığı (Time Complexity)**
  - O(1): Sabit zaman
  - O(log n): Logaritmik zaman
  - O(n): Doğrusal zaman
  - O(n²): Karesel zaman
  - O(2ⁿ): Üstel zaman

## 2. Veri Tipleri ve Değişkenler

### Temel Veri Tipleri

#### a) Tam Sayılar (Integer)
- byte: 8 bit (-128 ile 127)
- short: 16 bit
- int: 32 bit
- long: 64 bit

#### b) Ondalıklı Sayılar
- float: 32 bit
- double: 64 bit

#### c) Karakter (Char)
- Tek bir karakteri tutar
- 16 bit Unicode karakter

#### d) Boolean
- true/false değerlerini tutar
- 1 bit

#### e) String
- Karakter dizisi
- Metin verilerini tutar

### Değişken Tanımlama Kuralları
- Sayı ile başlayamaz
- Boşluk içeremez
- Özel karakter içeremez (_, $ hariç)
- Case sensitive'dir
- Reserved keyword'ler kullanılamaz

### Operatörler

#### a) Aritmetik Operatörler
- + (toplama)
- - (çıkarma)
- * (çarpma)
- / (bölme)
- % (mod alma)
- ++ (artırma)
- -- (azaltma)

#### b) İlişkisel Operatörler
- == (eşittir)
- != (eşit değildir)
- > (büyüktür)
- < (küçüktür)
- >= (büyük eşittir)
- <= (küçük eşittir)

#### c) Mantıksal Operatörler
- && (ve)
- || (veya)
- ! (değil)

## 3. Kontrol Yapıları

### If-Else Yapısı
```java
if (koşul) {
    // koşul doğruysa çalışır
} else if (başka koşul) {
    // ilk koşul yanlış, bu koşul doğruysa çalışır
} else {
    // hiçbir koşul doğru değilse çalışır
}
```

### Switch-Case Yapısı
```java
switch(değişken) {
    case değer1:
        // işlemler
        break;
    case değer2:
        // işlemler
        break;
    default:
        // hiçbir case uymazsa çalışır
}
```

### Döngüler

#### a) For Döngüsü
```java
for(başlangıç; koşul; artış/azalış) {
    // tekrar eden işlemler
}
```

#### b) While Döngüsü
```java
while(koşul) {
    // koşul doğru olduğu sürece çalışır
}
```

#### c) Do-While Döngüsü
```java
do {
    // en az bir kere çalışır
} while(koşul);
```

## 4. Fonksiyonlar/Metotlar

### Fonksiyon Tanımlama
```java
dönüş_tipi fonksiyon_adı(parametre_listesi) {
    // işlemler
    return değer;
}
```

### Parametre Geçirme Yöntemleri
- Call by Value: Değer ile çağırma
- Call by Reference: Referans ile çağırma

### Recursive (Özyinelemeli) Fonksiyonlar
- Kendini çağıran fonksiyonlar
- Base case (temel durum) mutlaka olmalı

Örnek (Faktöriyel):
```java
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n-1);
}
```

## 5. Diziler ve Koleksiyonlar

### Tek Boyutlu Diziler
```java
int[] dizi = new int[5];
// veya
int[] dizi = {1, 2, 3, 4, 5};
```

### Çok Boyutlu Diziler
```java
int[][] matris = new int[3][3];
// veya
int[][] matris = {{1,2,3}, {4,5,6}, {7,8,9}};
```

### Koleksiyonlar

#### a) ArrayList
```java
ArrayList<String> liste = new ArrayList<>();
liste.add("eleman");
liste.remove(0);
liste.get(0);
```

#### b) Stack (LIFO)
```java
Stack<Integer> stack = new Stack<>();
stack.push(5);
stack.pop();
stack.peek();
```

#### c) Queue (FIFO)
```java
Queue<String> kuyruk = new LinkedList<>();
kuyruk.offer("eleman");
kuyruk.poll();
kuyruk.peek();
```

## 6. Temel Algoritmalar

### Sıralama Algoritmaları

#### a) Bubble Sort
```java
void bubbleSort(int[] dizi) {
    for(int i = 0; i < dizi.length-1; i++)
        for(int j = 0; j < dizi.length-i-1; j++)
            if(dizi[j] > dizi[j+1]) {
                int temp = dizi[j];
                dizi[j] = dizi[j+1];
                dizi[j+1] = temp;
            }
}
```

#### b) Selection Sort
```java
void selectionSort(int[] dizi) {
    for(int i = 0; i < dizi.length-1; i++) {
        int min_idx = i;
        for(int j = i+1; j < dizi.length; j++)
            if(dizi[j] < dizi[min_idx])
                min_idx = j;
        int temp = dizi[min_idx];
        dizi[min_idx] = dizi[i];
        dizi[i] = temp;
    }
}
```

### Arama Algoritmaları

#### a) Linear Search
```java
int linearSearch(int[] dizi, int aranan) {
    for(int i = 0; i < dizi.length; i++)
        if(dizi[i] == aranan)
            return i;
    return -1;
}
```

#### b) Binary Search (Sıralı dizilerde)
```java
int binarySearch(int[] dizi, int aranan) {
    int left = 0, right = dizi.length - 1;
    while(left <= right) {
        int mid = (left + right) / 2;
        if(dizi[mid] == aranan) return mid;
        if(dizi[mid] < aranan) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## 7. Nesne Yönelimli Programlama

### Sınıf ve Nesne
```java
class Araba {
    // özellikler (attributes)
    String marka;
    String model;
    
    // constructor
    public Araba(String marka, String model) {
        this.marka = marka;
        this.model = model;
    }
    
    // metodlar
    void calistir() {
        System.out.println("Araba çalıştı");
    }
}
```

### Encapsulation (Kapsülleme)
```java
class BankaHesabi {
    private double bakiye;
    
    public double getBakiye() {
        return bakiye;
    }
    
    public void setBakiye(double miktar) {
        if(miktar > 0) {
            this.bakiye = miktar;
        }
    }
}
```

### Inheritance (Kalıtım)
```java
class Hayvan {
    void sesCikar() {
        System.out.println("Ses çıkarıyor");
    }
}

class Kopek extends Hayvan {
    @Override
    void sesCikar() {
        System.out.println("Hav hav!");
    }
}
```

## 8. Hata Yakalama

### Try-Catch Yapısı
```java
try {
    // hata oluşabilecek kod
} catch(Exception e) {
    // hata yakalandığında çalışacak kod
} finally {
    // her durumda çalışacak kod
}
```

### Exception Tipleri
- ArithmeticException
- ArrayIndexOutOfBoundsException
- NullPointerException
- FileNotFoundException
- IOException

## 9. Temel Veri Yapıları

### Stack (Yığın)
- LIFO (Last In First Out) prensibi
- Push: Ekleme
- Pop: Çıkarma
- Peek: En üstteki elemanı görme

### Queue (Kuyruk)
- FIFO (First In First Out) prensibi
- Enqueue: Ekleme
- Dequeue: Çıkarma
- Peek: İlk elemanı görme

### Linked List (Bağlı Liste)
- Her düğüm veri ve sonraki düğümün referansını tutar
- Ekleme ve silme işlemleri dinamik
- Baştan, ortadan ve sondan ekleme/silme yapılabilir

## 10. Dosya İşlemleri

### Dosya Okuma
```java
try {
    BufferedReader reader = new BufferedReader(new FileReader("dosya.txt"));
    String satir;
    while((satir = reader.readLine()) != null) {
        System.out.println(satir);
    }
    reader.close();
} catch(IOException e) {
    e.printStackTrace();
}
```

### Dosya Yazma
```java
try {
    BufferedWriter writer = new BufferedWriter(new FileWriter("dosya.txt"));
    writer.write("Merhaba Dünya!");
    writer.close();
} catch(IOException e) {
    e.printStackTrace();
}
```
