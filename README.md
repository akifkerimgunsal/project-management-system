# Proje Yönetim Sistemi

Bu proje, modern bir proje yönetim sistemi uygulamasıdır. Kullanıcıların projeler oluşturmasına, görevleri yönetmesine ve ekip üyeleriyle işbirliği yapmasına olanak tanır. Flask tabanlı bir backend API ve Vue.js tabanlı bir frontend arayüzü içerir.

![Proje Yönetim Sistemi]

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Teknoloji Yığını](#teknoloji-yığını)
- [Sistem Mimarisi](#sistem-mimarisi)
- [Kurulum](#kurulum)
  - [Gereksinimler](#gereksinimler)
  - [Backend Kurulumu](#backend-kurulumu)
  - [Frontend Kurulumu](#frontend-kurulumu)
- [Kullanım](#kullanım)
- [API Dokümantasyonu](#api-dokümantasyonu)
- [Veri Modeli](#veri-modeli)

## Özellikler

- **Kullanıcı Yönetimi**: Kayıt olma, giriş yapma ve kullanıcı profili yönetimi
- **Proje Yönetimi**: Projeler oluşturma, düzenleme ve silme
- **Görev Yönetimi**: Görevler oluşturma, atama, düzenleme ve takip etme
- **Pano Sistemi**: Görevleri kanban tarzı panolarda organize etme
- **Ekip İşbirliği**: Projelere ve görevlere ekip üyelerini davet etme
- **Denetim Günlüğü**: Sistem üzerindeki tüm değişikliklerin kaydını tutma
- **Responsive Tasarım**: Mobil cihazlar dahil tüm ekran boyutlarına uyumlu arayüz

## Teknoloji Yığını

### Backend
- **Python 3.8+**
- **Flask**: Web çerçevesi
- **SQLAlchemy**: ORM (Nesne İlişkisel Eşleyici)
- **Flask-JWT-Extended**: Kimlik doğrulama ve yetkilendirme
- **Flask-Migrate**: Veritabanı şema migrasyonları
- **Flask-CORS**: Cross-Origin Resource Sharing desteği

### Frontend
- **Vue.js 3**: Progressive JavaScript çerçevesi
- **Vuetify 3**: Material Design bileşen kütüphanesi
- **Vue Router**: Sayfa yönlendirme
- **Axios**: HTTP istekleri
- **Vite**: Build aracı

### Veritabanı
- **SQLite** (Geliştirme)
- **PostgreSQL** (Üretim)

## Sistem Mimarisi

Proje, modern bir katmanlı mimari kullanılarak geliştirilmiştir:

```
├── Backend (Flask)
│   ├── API Katmanı (api/)
│   ├── İş Mantığı Katmanı (business/)
│   ├── Veri Erişim Katmanı (data_access/)
│   ├── Varlık Katmanı (entities/)
│   └── Yardımcı Araçlar (helpers/)
│
└── Frontend (Vue.js)
    ├── Bileşenler (components/)
    ├── Görünümler (views/)
    ├── Servisler (services/)
    ├── Yönlendirme (router/)
    └── Varlıklar (assets/)
```

## Kurulum

### Gereksinimler

- Python 3.8 veya üstü
- Node.js 16 veya üstü
- npm 8 veya üstü
- Git

### Backend Kurulumu

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/proje-yonetim-sistemi.git
   cd proje-yonetim-sistemi
   ```

2. Python sanal ortamı oluşturun ve etkinleştirin:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. Veritabanını oluşturun ve migrasyon yapın:
   ```bash
   flask db upgrade
   ```

5. Uygulamayı başlatın:
   ```bash
   python app.py
   ```
   
   Backend API http://localhost:5000 adresinde çalışacaktır.

### Frontend Kurulumu

1. Frontend dizinine gidin:
   ```bash
   cd frontend/project-management-system
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```

3. Geliştirme sunucusunu başlatın:
   ```bash
   npm run dev
   ```
   
   Frontend uygulaması http://localhost:5173 adresinde çalışacaktır.

## Kullanım

### Kullanıcı Kaydı ve Giriş

1. Tarayıcınızda http://localhost:5173 adresine gidin
2. "Kayıt Ol" butonuna tıklayın ve gerekli bilgileri doldurun
3. Kayıt olduktan sonra, e-posta ve şifrenizle giriş yapın

### Proje Oluşturma

1. Ana sayfada "Yeni Proje" butonuna tıklayın
2. Proje adı, açıklaması ve diğer detayları girin
3. "Oluştur" butonuna tıklayın

### Görev Oluşturma ve Yönetme

1. Bir projeye tıklayın
2. "Yeni Görev" butonuna tıklayın
3. Görev başlığı, açıklaması, atanan kişi ve son tarihi girin
4. Görevleri sürükle-bırak ile farklı durumlara taşıyabilirsiniz

## API Dokümantasyonu

### Kimlik Doğrulama

```
POST /api/auth/register - Yeni kullanıcı kaydı
POST /api/auth/login - Kullanıcı girişi
POST /api/auth/refresh - Token yenileme
POST /api/auth/logout - Çıkış yapma
```

### Projeler

```
GET /api/projects - Tüm projeleri listele
POST /api/projects - Yeni proje oluştur
GET /api/projects/{id} - Proje detaylarını getir
PUT /api/projects/{id} - Proje güncelle
DELETE /api/projects/{id} - Proje sil
```

### Panolar

```
GET /api/boards - Tüm panoları listele
POST /api/boards - Yeni pano oluştur
GET /api/boards/{id} - Pano detaylarını getir
PUT /api/boards/{id} - Pano güncelle
DELETE /api/boards/{id} - Pano sil
```

### Görevler

```
GET /api/tasks - Tüm görevleri listele
POST /api/tasks - Yeni görev oluştur
GET /api/tasks/{id} - Görev detaylarını getir
PUT /api/tasks/{id} - Görev güncelle
DELETE /api/tasks/{id} - Görev sil
```

##  Veri Modeli

Proje aşağıdaki ana veri modellerini kullanır:

- **User**: Kullanıcı bilgileri
- **Project**: Proje bilgileri
- **Board**: Kanban panoları
- **Task**: Görevler
- **AuditLog**: Sistem değişiklik kayıtları
- **RefreshToken**: JWT yenileme tokenları

İlişkiler:
- Bir kullanıcı birden çok projeye sahip olabilir
- Bir proje birden çok panoya sahip olabilir
- Bir pano birden çok göreve sahip olabilir
- Bir görev bir kullanıcıya atanabilir

⭐️ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın! ⭐️ 
