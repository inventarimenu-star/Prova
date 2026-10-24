/* Boulevard TV — cilësimet. Çmimet NUK shkruhen këtu: merren live nga sistemi (vetëm lexim).
   Këtu zgjedhim VETËM çfarë del në ekran dhe me çfarë emri. */
window.TV_CONFIG = {
  db: {
    url: 'https://c--58dc0c87-3008-4bdc-85e3-82d8c17aeb57-prod.lovable.cloud',
    key: 'sb_publishable_Wq2dUS_Y4EVTcSOQggwBhg_3grIeO_s' // çelës publik (i njëjti që përdor menuja e klientit)
  },
  /* Fotot dhe videot merren nga GitHub (dosja tv/ e projektit). */
  mediaBase: 'https://raw.githubusercontent.com/inventarimenu-star/Prova/main/tv/',
  seconds: 10,          // sa sekonda qëndron çdo ekran
  phone: '067 401 0030',
  timezone: 'Europe/Tirane',

  /* Ekranet, sipas radhës. Një ekran "offer" del VETËM kur oferta është aktive në sistem dhe brenda orarit të saj.
     items: [emri në sistem, emri në TV]. Artikujt që mungojnë ose s'janë në ofertë nuk shfaqen. */
  slides: [
    { type: 'offer', offer: 'Oferta e Mëngjesit', kicker: 'OFERTA E MËNGJESIT', title: 'Fillo ditën me ne', theme: 'gold',
      footer: 'E 10-ta kafe FALAS kur porosit nga telefoni',
      items: [['KAFE expres', 'Kafe ekspres'], ['KAFE MAKIATO', 'Makiato'], ['KAPUCHINO ME KAFE', 'Kapuçino'],
              ['Briosh', 'Briosh'], ['ÇOKOLLATE', 'Çokollatë'], ['CAJ I NXEHTË BIO', 'Çaj bio']] },
    { type: 'image', src: 'media/poster-mengjesi.jpg', offer: 'Oferta e Mëngjesit' },   // poster CapCut (del vetëm 07–11)
    { type: 'product', offer: 'Oferta e Mëngjesit', item: 'KAFE expres', label: 'Kafe ekspres', kicker: 'MËNGJESI',
      photo: 'media/espresso.jpg', layout: 'full', theme: 'gold' },

    { type: 'offer', offer: 'Oferta e Drekës 🍕', kicker: 'OFERTA E DREKËS', title: 'Pizza 100 lekë më lirë', theme: 'orange',
      footer: 'Porosit nga telefoni: skano QR-në në tavolinë',
      items: [['Pizza Margarita', 'Pizza Margarita'], ['Pizza Kapricoza', 'Pizza Kapricoza'], ['Pizza Tono', 'Pizza Tono'],
              ['Pizza 4 Djatherat', 'Pizza 4 Djathërat'], ['Chicken Wings', 'Chicken Wings'], ['Chiken Finger', 'Chicken Finger']] },
    { type: 'product', offer: 'Oferta e Drekës 🍕', item: 'Pizza Margarita', label: 'Pizza Margarita', kicker: 'DREKA',
      photo: 'media/food-pizza-clean.jpg', layout: 'side', theme: 'orange' },
    { type: 'video', src: 'media/reel-pizza.mp4', offer: 'Oferta e Drekës 🍕', kicker: 'DREKA', title: 'Pizza e freskët', theme: 'orange' },

    { type: 'offer', offer: '🍺 & 🍷', kicker: 'BIRRA & VERË', title: 'Birrat belge premium me çmimin e një Heineken-i', theme: 'green',
      footer: 'Skano QR-në në faturë: mund të jesh fitues!',
      items: [['Duvel Beer', 'Duvel'], ['Blenche de Namy', 'Blanche'], ['HEINEKEN SHISHE 400ml', 'Heineken shishe'],
              ['KRIKO Heineken 400ml', 'Heineken kriko'], ['Birra Moretti 330ml', 'Moretti'], ['GOTE VERE', 'Gotë verë']] },

    { type: 'video', src: 'media/reel-kafeja.mp4', kicker: 'BOULEVARD CAFFE', title: 'Kafeja jonë', theme: 'gold' },
    { type: 'matches' },
    { type: 'loyalty', active: true },
    { type: 'image', src: 'media/poster-besnikeria.jpg', active: true },              // poster CapCut i besnikërisë (QR i vërtetë)
    { type: 'notice', active: true, kicker: 'NJOFTIM', title: 'Kërkojmë kamarier/e', sub: 'Për turnin e parë (mëngjes)',
      pill: 'Aplikoni: 067 401 0030', note: 'Telefononi, shkruani në WhatsApp ose ejani në lokal' }
  ],

  /* Ndeshjet: shfaqen vetëm ditën e shënuar (date = YYYY-MM-DD). */
  matches: {
    date: '2026-10-24',
    offerLine: 'Heineken 200 lekë · shishe ose kriko',
    list: [
      // ['ORA', 'Shtëpia', 'Mysafiri', 'Kampionati']  (stemat merren vetë nga media/logos/)
      ['13:30', 'Aston Villa', 'Man City', 'Premier League'],
      ['13:30', 'Partizani', 'Skënderbeu', 'Abissnet Superiore'],
      ['13:30', 'Laçi', 'Vora', 'Abissnet Superiore'],
      ['16:00', 'Arsenal', 'Everton', 'Premier League'],
      ['18:00', 'Napoli', 'Roma', 'Serie A'],
      ['18:30', 'Teuta', 'AF Elbasani', 'Abissnet Superiore'],
      ['18:30', 'Vllaznia', 'Tirana', 'Abissnet Superiore'],
      ['18:30', 'Chelsea', 'Tottenham', 'Premier League'],
      ['21:00', 'Atletico Madrid', 'Deportivo', 'La Liga']
    ]
  },

  /* REKLAMA (biznese të tjera ose të tuat). Del çdo "every" ekrane, vetëm nga "from" deri "to".
     image: foto 16:9 (1920×1080) ose video: 'media/...mp4'. Shembull:
     { name: 'Dyqani X', image: 'media/reklama-dyqani-x.jpg', from: '2026-11-01', to: '2026-11-30', every: 4 } */
  ads: []
};
