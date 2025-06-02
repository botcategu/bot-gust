from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import json
import time
import threading
from datetime import datetime
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura'

# Configuración global del bot
BOT_CONFIG = {
    'admin_password':
    'admin123',  # Cambia esta contraseña
    'store_url':
    'https://tu-tienda.com',
    'store_name':
    'Mi Tienda Online',
    'custom_domain':
    '',  # Dominio personalizado
    'target_keywords': ['comprar online', 'tienda', 'productos', 'ofertas'],
    'languages': [
        'es', 'en', 'fr', 'de', 'pt', 'it', 'zh', 'ja', 'ko', 'ar', 'ru', 'hi',
        'th', 'vi', 'tr', 'pl', 'nl', 'sv', 'da', 'no'
    ],
    'social_networks': [
        'twitter', 'facebook', 'instagram', 'linkedin', 'youtube', 'tiktok',
        'pinterest', 'reddit', 'telegram', 'whatsapp', 'snapchat', 'discord',
        'tumblr', 'vkontakte', 'weibo', 'line', 'viber', 'clubhouse', 'twitch',
        'mastodon', 'threads', 'bluesky'
    ],
    'search_engines': [
        'google', 'bing', 'yahoo', 'duckduckgo', 'yandex', 'baidu', 'ask',
        'ecosia', 'startpage', 'searx', 'brave', 'qwant'
    ],
    'countries': {
        'España': {
            'code':
            'ES',
            'language':
            'es',
            'states': [
                'Madrid', 'Cataluña', 'Valencia', 'Andalucía', 'País Vasco',
                'Galicia', 'Aragón', 'Castilla y León', 'Murcia', 'Asturias'
            ]
        },
        'Estados Unidos': {
            'code':
            'US',
            'language':
            'en',
            'states': [
                'California', 'Texas', 'Florida', 'New York', 'Illinois',
                'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan'
            ]
        },
        'México': {
            'code':
            'MX',
            'language':
            'es',
            'states': [
                'Ciudad de México', 'Jalisco', 'Nuevo León', 'Puebla',
                'Guanajuato', 'Veracruz', 'Chihuahua', 'Baja California',
                'Sonora', 'Coahuila'
            ]
        },
        'Argentina': {
            'code':
            'AR',
            'language':
            'es',
            'states': [
                'Buenos Aires', 'Córdoba', 'Santa Fe', 'Mendoza', 'Tucumán',
                'Entre Ríos', 'Salta', 'Misiones', 'Corrientes',
                'Santiago del Estero'
            ]
        },
        'Colombia': {
            'code':
            'CO',
            'language':
            'es',
            'states': [
                'Bogotá', 'Antioquia', 'Valle del Cauca', 'Atlántico',
                'Santander', 'Bolívar', 'Cundinamarca', 'Norte de Santander',
                'Córdoba', 'Tolima'
            ]
        },
        'Francia': {
            'code':
            'FR',
            'language':
            'fr',
            'states': [
                'Île-de-France', 'Provence-Alpes-Côte d\'Azur',
                'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie',
                'Hauts-de-France', 'Grand Est', 'Pays de la Loire', 'Bretagne',
                'Normandie'
            ]
        },
        'Alemania': {
            'code':
            'DE',
            'language':
            'de',
            'states': [
                'Bayern', 'Nordrhein-Westfalen', 'Baden-Württemberg',
                'Niedersachsen', 'Hessen', 'Sachsen', 'Rheinland-Pfalz',
                'Berlin', 'Schleswig-Holstein', 'Brandenburg'
            ]
        },
        'Italia': {
            'code':
            'IT',
            'language':
            'it',
            'states': [
                'Lombardia', 'Lazio', 'Campania', 'Sicilia', 'Veneto',
                'Piemonte', 'Emilia-Romagna', 'Puglia', 'Toscana', 'Calabria'
            ]
        },
        'Brasil': {
            'code':
            'BR',
            'language':
            'pt',
            'states': [
                'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia',
                'Paraná', 'Rio Grande do Sul', 'Pernambuco', 'Ceará', 'Pará',
                'Santa Catarina'
            ]
        },
        'Reino Unido': {
            'code': 'GB',
            'language': 'en',
            'states': ['England', 'Scotland', 'Wales', 'Northern Ireland']
        },
        'Canadá': {
            'code':
            'CA',
            'language':
            'en',
            'states': [
                'Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba',
                'Saskatchewan', 'Nova Scotia', 'New Brunswick',
                'Newfoundland and Labrador', 'Prince Edward Island'
            ]
        },
        'China': {
            'code':
            'CN',
            'language':
            'zh',
            'states': [
                'Beijing', 'Shanghai', 'Guangdong', 'Zhejiang', 'Jiangsu',
                'Shandong', 'Henan', 'Sichuan', 'Hebei', 'Hunan'
            ]
        },
        'Japón': {
            'code':
            'JP',
            'language':
            'ja',
            'states': [
                'Tokyo', 'Osaka', 'Kanagawa', 'Aichi', 'Saitama', 'Chiba',
                'Hyogo', 'Hokkaido', 'Fukuoka', 'Shizuoka'
            ]
        },
        'Corea del Sur': {
            'code':
            'KR',
            'language':
            'ko',
            'states': [
                'Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju',
                'Ulsan', 'Gyeonggi', 'Gangwon', 'Chungcheong'
            ]
        },
        'Australia': {
            'code':
            'AU',
            'language':
            'en',
            'states': [
                'New South Wales', 'Victoria', 'Queensland',
                'Western Australia', 'South Australia', 'Tasmania',
                'Australian Capital Territory', 'Northern Territory'
            ]
        },
        'India': {
            'code':
            'IN',
            'language':
            'hi',
            'states': [
                'Maharashtra', 'Tamil Nadu', 'Karnataka', 'Gujarat',
                'Rajasthan', 'West Bengal', 'Andhra Pradesh', 'Uttar Pradesh',
                'Kerala', 'Telangana'
            ]
        },
        'Rusia': {
            'code':
            'RU',
            'language':
            'ru',
            'states': [
                'Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg',
                'Nizhny Novgorod', 'Kazan', 'Chelyabinsk', 'Omsk', 'Samara',
                'Rostov-on-Don'
            ]
        },
        'Tailandia': {
            'code':
            'TH',
            'language':
            'th',
            'states': [
                'Bangkok', 'Chiang Mai', 'Chon Buri', 'Rayong', 'Khon Kaen',
                'Nakhon Ratchasima', 'Songkhla', 'Udon Thani', 'Surat Thani',
                'Nonthaburi'
            ]
        },
        'Vietnam': {
            'code':
            'VN',
            'language':
            'vi',
            'states': [
                'Ho Chi Minh City', 'Hanoi', 'Hai Phong', 'Da Nang',
                'Bien Hoa', 'Hue', 'Nha Trang', 'Can Tho', 'Rach Gia',
                'Qui Nhon'
            ]
        },
        'Turquía': {
            'code':
            'TR',
            'language':
            'tr',
            'states': [
                'Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Adana', 'Gaziantep',
                'Konya', 'Antalya', 'Diyarbakir', 'Mersin'
            ]
        },
        'Polonia': {
            'code':
            'PL',
            'language':
            'pl',
            'states': [
                'Mazowieckie', 'Śląskie', 'Wielkopolskie', 'Małopolskie',
                'Dolnośląskie', 'Łódzkie', 'Kujawsko-Pomorskie', 'Pomorskie',
                'Podlaskie', 'Zachodniopomorskie'
            ]
        },
        'Países Bajos': {
            'code':
            'NL',
            'language':
            'nl',
            'states': [
                'Noord-Holland', 'Zuid-Holland', 'Noord-Brabant', 'Gelderland',
                'Utrecht', 'Overijssel', 'Limburg', 'Friesland', 'Groningen',
                'Drenthe'
            ]
        },
        'Suecia': {
            'code':
            'SE',
            'language':
            'sv',
            'states': [
                'Stockholm', 'Västra Götaland', 'Skåne', 'Uppsala',
                'Östergötland', 'Jönköping', 'Halland', 'Örebro', 'Gävleborg',
                'Dalarna'
            ]
        },
        'Dinamarca': {
            'code':
            'DK',
            'language':
            'da',
            'states': [
                'Capital Region', 'Central Denmark', 'North Denmark',
                'Zealand', 'Southern Denmark'
            ]
        },
        'Noruega': {
            'code':
            'NO',
            'language':
            'no',
            'states': [
                'Oslo', 'Viken', 'Rogaland', 'Møre og Romsdal', 'Nordland',
                'Vestland', 'Innlandet', 'Vestfold og Telemark', 'Agder',
                'Trøndelag'
            ]
        }
    },
    'active':
    True,
    'search_interval':
    300,  # 5 minutos
    'daily_targets':
    100,
    'destinations': [{
        'name': 'Tienda A',
        'url': 'https://tienda-a.com',
        'active': True
    }, {
        'name': 'Tienda B',
        'url': 'https://tienda-b.com',
        'active': False
    }, {
        'name': 'Tienda C',
        'url': 'https://tienda-c.com',
        'active': True
    }]
}

# Base de datos en memoria para clientes potenciales
POTENTIAL_CLIENTS = []
BOT_STATS = {
    'clients_found': 0,
    'messages_sent': 0,
    'conversions': 0,
    'last_activity': None,
    'start_time': datetime.now()
}

# Base de datos para campañas
CAMPAIGNS = []

# Base de datos para analytics
ANALYTICS_DATA = {
    'hourly_clients': {
        'labels': [],
        'data': []
    },
    'networks_distribution': {},
    'performance_hourly': [],
    'languages_distribution': {},
    'total_clients': 0,
    'conversion_rate': 0,
    'messages_per_hour': 0,
    'best_network': 'N/A'
}

# Base de datos para enlaces de redes sociales
SOCIAL_LINKS = []

# Base de datos para múltiples bots
BOTS_DATABASE = [{
    'id':
    1,
    'name':
    'Bot Principal',
    'description':
    'Bot principal para captación de clientes',
    'objective':
    'clientes',
    'status':
    'activo',
    'created_date':
    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'last_activity':
    None,
    'clients_found':
    0,
    'messages_sent':
    0,
    'conversions':
    0,
    'target_countries': [],
    'target_languages': ['es', 'en'],
    'target_networks': ['facebook', 'instagram', 'twitter'],
    'tasks': [
        'Buscar clientes en redes sociales', 'Enviar mensajes personalizados',
        'Seguimiento de conversiones'
    ]
}]


class ClientHunterBot:

    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._hunt_clients)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False

    def _hunt_clients(self):
        while self.running and BOT_CONFIG['active']:
            try:
                # Simular búsqueda en redes sociales
                self._search_social_media()
                # Simular búsqueda en motores de búsqueda
                self._search_engines()
                # Esperar antes de la próxima búsqueda
                time.sleep(BOT_CONFIG['search_interval'])
            except Exception as e:
                print(f"Error en bot: {e}")
                time.sleep(60)

    def _search_social_media(self):
        import random
        countries = list(BOT_CONFIG['countries'].keys())

        for network in BOT_CONFIG['social_networks']:
            for keyword in BOT_CONFIG['target_keywords']:
                for lang in BOT_CONFIG['languages']:
                    # Seleccionar país aleatorio
                    country = random.choice(countries)
                    country_info = BOT_CONFIG['countries'][country]
                    state = random.choice(country_info['states'])

                    # Simular encontrar clientes potenciales
                    potential_client = {
                        'id': len(POTENTIAL_CLIENTS) + 1,
                        'source': network,
                        'keyword': keyword,
                        'language': lang,
                        'country': country,
                        'state': state,
                        'country_code': country_info['code'],
                        'contact':
                        f"user_{len(POTENTIAL_CLIENTS)}@{network}.com",
                        'timestamp':
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'nuevo',
                        'interest_level': 'alto',
                        'campaign_type': 'social_media'
                    }
                    POTENTIAL_CLIENTS.append(potential_client)
                    BOT_STATS['clients_found'] += 1
                    BOT_STATS['last_activity'] = datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S')

                    # Simular envío de mensaje personalizado
                    self._send_personalized_message(potential_client)

                    if len(POTENTIAL_CLIENTS) >= BOT_CONFIG['daily_targets']:
                        return

    def _search_engines(self):
        import random
        countries = list(BOT_CONFIG['countries'].keys())

        # Simular búsqueda en múltiples motores de búsqueda
        for engine in BOT_CONFIG['search_engines']:
            for keyword in BOT_CONFIG['target_keywords']:
                for lang in BOT_CONFIG['languages']:
                    # Seleccionar país aleatorio
                    country = random.choice(countries)
                    country_info = BOT_CONFIG['countries'][country]
                    state = random.choice(country_info['states'])

                    # Simular encontrar leads en motores de búsqueda
                    potential_client = {
                        'id': len(POTENTIAL_CLIENTS) + 1,
                        'source': engine,
                        'keyword': keyword,
                        'language': lang,
                        'country': country,
                        'state': state,
                        'country_code': country_info['code'],
                        'contact':
                        f"lead_{len(POTENTIAL_CLIENTS)}@{engine}.com",
                        'timestamp':
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'nuevo',
                        'interest_level': 'medio',
                        'campaign_type': 'search_engine'
                    }
                    POTENTIAL_CLIENTS.append(potential_client)
                    BOT_STATS['clients_found'] += 1
                    BOT_STATS['last_activity'] = datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S')

                    # Simular envío de mensaje personalizado
                    self._send_personalized_message(potential_client)

                    if len(POTENTIAL_CLIENTS) >= BOT_CONFIG['daily_targets']:
                        return

    def _send_personalized_message(self, client):
        # Seleccionar destino activo aleatorio
        active_destinations = [
            d for d in BOT_CONFIG['destinations'] if d['active']
        ]
        if not active_destinations:
            active_destinations = BOT_CONFIG[
                'destinations'][:1]  # Usar el primero como fallback

        import random
        destination = random.choice(active_destinations)

        # Mensajes personalizados por idioma
        messages = {
            'es':
            f"¡Hola! He visto tu interés en {client['keyword']}. Te invito a conocer {destination['name']} con ofertas especiales: {destination['url']}",
            'en':
            f"Hello! I saw your interest in {client['keyword']}. I invite you to check {destination['name']} with special offers: {destination['url']}",
            'fr':
            f"Salut! J'ai vu votre intérêt pour {client['keyword']}. Je vous invite à découvrir {destination['name']}: {destination['url']}",
            'de':
            f"Hallo! Ich habe Ihr Interesse an {client['keyword']} gesehen. Besuchen Sie {destination['name']}: {destination['url']}",
            'pt':
            f"Olá! Vi seu interesse em {client['keyword']}. Convido você a conhecer {destination['name']}: {destination['url']}",
            'it':
            f"Ciao! Ho visto il tuo interesse per {client['keyword']}. Ti invito a scoprire {destination['name']}: {destination['url']}",
            'zh':
            f"你好！我看到你对{client['keyword']}感兴趣。邀请你了解{destination['name']}的特别优惠：{destination['url']}",
            'ja':
            f"こんにちは！{client['keyword']}にご興味をお持ちいただき、{destination['name']}の特別オファーをご覧ください：{destination['url']}",
            'ko':
            f"안녕하세요! {client['keyword']}에 관심이 있으신 것을 보았습니다. {destination['name']}의 특별 혜택을 확인해보세요: {destination['url']}",
            'ar':
            f"مرحبا! لقد رأيت اهتمامك بـ {client['keyword']}. أدعوك لاكتشاف {destination['name']} مع عروض خاصة: {destination['url']}"
        }

        message = messages.get(client['language'], messages['es'])
        # Simular envío
        BOT_STATS['messages_sent'] += 1
        print(f"Mensaje enviado a {client['contact']}: {message}")

        # Agregar información del destino al cliente
        client['destination_used'] = destination['name']
        client['destination_url'] = destination['url']


# Instancia del bot
client_hunter = ClientHunterBot()


@app.route('/')
def login_page():
    if 'authenticated' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == BOT_CONFIG['admin_password']:
        session['authenticated'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Contraseña incorrecta')


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login_page'))


@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html',
                           config=BOT_CONFIG,
                           stats=BOT_STATS)


@app.route('/clients')
def clients():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('clients.html', clients=POTENTIAL_CLIENTS)


@app.route('/config')
def config():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('config.html', config=BOT_CONFIG)


@app.route('/campaigns')
def campaigns():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('campaigns.html', campaigns=CAMPAIGNS)


@app.route('/analytics')
def analytics():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('analytics.html')


@app.route('/bots')
def bots_management():
    if 'authenticated' not in session:
        return redirect(url_for('login_page'))
    return render_template('bots.html', bots=BOTS_DATABASE)


@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    client_hunter.start()
    return jsonify({'success': True, 'message': 'Bot iniciado'})


@app.route('/api/stop_bot', methods=['POST'])
def stop_bot():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    client_hunter.stop()
    return jsonify({'success': True, 'message': 'Bot detenido'})


@app.route('/api/update_config', methods=['POST'])
def update_config():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.json
    BOT_CONFIG.update(data)
    return jsonify({'success': True, 'message': 'Configuración actualizada'})


@app.route('/api/stats')
def get_stats():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    return jsonify(BOT_STATS)


@app.route('/api/clients')
def get_clients():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    return jsonify(POTENTIAL_CLIENTS[-50:])  # Últimos 50 clientes


@app.route('/api/create_campaign', methods=['POST'])
def create_campaign():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.json
    campaign = {
        'id': len(CAMPAIGNS) + 1,
        'name': data.get('name'),
        'description': data.get('description'),
        'campaign_type': data.get('campaign_type', 'general'),
        'target_keywords': data.get('target_keywords', []),
        'target_languages': data.get('target_languages', []),
        'target_networks': data.get('target_networks', []),
        'target_engines': data.get('target_engines', []),
        'target_countries': data.get('target_countries', []),
        'target_states': data.get('target_states', []),
        'use_all_countries': data.get('use_all_countries', False),
        'objective': data.get('objective', 'clientes'),
        'custom_message': data.get('custom_message'),
        'status': data.get('status', 'activa'),
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'clients_targeted': 0,
        'conversions': 0,
        'followers_gained': 0,
        'engagement_rate': 0
    }
    CAMPAIGNS.append(campaign)
    return jsonify({'success': True, 'campaign': campaign})


@app.route('/api/campaigns')
def get_campaigns():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    return jsonify(CAMPAIGNS)


@app.route('/api/toggle_campaign/<int:campaign_id>', methods=['POST'])
def toggle_campaign(campaign_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    for campaign in CAMPAIGNS:
        if campaign['id'] == campaign_id:
            campaign['status'] = 'inactiva' if campaign[
                'status'] == 'activa' else 'activa'
            return jsonify({'success': True, 'status': campaign['status']})

    return jsonify({'error': 'Campaña no encontrada'}), 404


@app.route('/api/delete_campaign/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    global CAMPAIGNS
    CAMPAIGNS = [c for c in CAMPAIGNS if c['id'] != campaign_id]
    return jsonify({'success': True})


@app.route('/api/analytics')
def get_analytics():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    # Generar datos de analytics en tiempo real
    import random
    from datetime import datetime, timedelta

    # Datos por hora (últimas 24 horas)
    now = datetime.now()
    hourly_labels = []
    hourly_data = []

    for i in range(24):
        hour = now - timedelta(hours=23 - i)
        hourly_labels.append(hour.strftime('%H:%M'))
        hourly_data.append(random.randint(0, 20))

    # Distribución por redes sociales
    networks_dist = {}
    for network in BOT_CONFIG['social_networks'][:8]:  # Top 8 redes
        networks_dist[network] = random.randint(5, 50)

    # Distribución por motores de búsqueda
    engines_dist = {}
    for engine in BOT_CONFIG['search_engines'][:6]:  # Top 6 motores
        engines_dist[engine] = random.randint(10, 80)

    # Distribución por idiomas
    languages_dist = {}
    for lang in BOT_CONFIG['languages'][:6]:  # Top 6 idiomas
        languages_dist[lang] = random.randint(10, 100)

    # Calcular métricas
    total_clients = len(POTENTIAL_CLIENTS)
    conversion_rate = round(random.uniform(2.5, 8.5), 1)
    messages_per_hour = round(BOT_STATS['messages_sent'] / max(1, 24), 1)
    best_network = max(networks_dist.keys(), key=lambda k: networks_dist[k])

    analytics_data = {
        'hourly_clients': {
            'labels': hourly_labels,
            'data': hourly_data
        },
        'networks_distribution': networks_dist,
        'engines_distribution': engines_dist,
        'languages_distribution': languages_dist,
        'total_clients': total_clients,
        'conversion_rate': conversion_rate,
        'messages_per_hour': messages_per_hour,
        'best_network': best_network.title()
    }

    return jsonify(analytics_data)


@app.route('/api/social-links', methods=['GET', 'POST'])
def social_links():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    if request.method == 'POST':
        link_data = request.json
        link_data['id'] = len(SOCIAL_LINKS) + 1
        SOCIAL_LINKS.append(link_data)
        return jsonify({'success': True, 'link': link_data})

    return jsonify(SOCIAL_LINKS)


@app.route('/api/social-links/<int:link_id>', methods=['DELETE'])
def delete_social_link(link_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    global SOCIAL_LINKS
    SOCIAL_LINKS = [
        link for i, link in enumerate(SOCIAL_LINKS) if i != link_id
    ]
    return jsonify({'success': True})


@app.route('/api/bots', methods=['GET', 'POST'])
def manage_bots():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    if request.method == 'POST':
        bot_data = request.json
        new_bot = {
            'id': len(BOTS_DATABASE) + 1,
            'name': bot_data.get('name'),
            'description': bot_data.get('description'),
            'objective': bot_data.get('objective'),
            'status': 'inactivo',
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_activity': None,
            'clients_found': 0,
            'messages_sent': 0,
            'conversions': 0,
            'target_countries': bot_data.get('target_countries', []),
            'target_languages': bot_data.get('target_languages', []),
            'target_networks': bot_data.get('target_networks', []),
            'tasks': bot_data.get('tasks', [])
        }
        BOTS_DATABASE.append(new_bot)
        return jsonify({'success': True, 'bot': new_bot})

    return jsonify(BOTS_DATABASE)


@app.route('/api/bots/<int:bot_id>/toggle', methods=['POST'])
def toggle_bot(bot_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    for bot in BOTS_DATABASE:
        if bot['id'] == bot_id:
            bot['status'] = 'inactivo' if bot[
                'status'] == 'activo' else 'activo'
            if bot['status'] == 'activo':
                bot['last_activity'] = datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')
            return jsonify({'success': True, 'status': bot['status']})

    return jsonify({'error': 'Bot no encontrado'}), 404


@app.route('/api/bots/<int:bot_id>', methods=['PUT', 'DELETE'])
def update_delete_bot(bot_id):
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    if request.method == 'DELETE':
        global BOTS_DATABASE
        BOTS_DATABASE = [bot for bot in BOTS_DATABASE if bot['id'] != bot_id]
        return jsonify({'success': True})

    if request.method == 'PUT':
        bot_data = request.json
        for bot in BOTS_DATABASE:
            if bot['id'] == bot_id:
                bot.update(bot_data)
                return jsonify({'success': True, 'bot': bot})

        return jsonify({'error': 'Bot no encontrado'}), 404


@app.route('/api/countries')
def get_countries():
    if 'authenticated' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    return jsonify(BOT_CONFIG['countries'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
