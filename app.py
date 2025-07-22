from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)

penyakit = ['Anemia', 'Bronkhitis', 'Flu', 'Demam']
gejala = ['Badan Panas', 'Sakit Kepala', 'Bersin-bersin', 'Batuk', 'Pilek, Hidung Buntu', 'Badan Lemas', 'Kedinginan']

pengetahuan = [
    ['Anemia', 'Sakit Kepala', 0.7, 0.2],
    ['Anemia', 'Badan Lemas', 0.8, 0.1],
    ['Bronkhitis', 'Badan Panas', 0.6, 0.2],
    ['Bronkhitis', 'Bersin-bersin', 0.7, 0.4],
    ['Bronkhitis', 'Batuk', 0.8, 0.1],
    ['Demam', 'Kedinginan', 0.7, 0.1],
    ['Demam', 'Badan Lemas', 0.6, 0.2],
    ['Demam', 'Badan Panas', 0.8, 0.1],
    ['Flu', 'Badan Panas', 0.6, 0.2],
    ['Flu', 'Sakit Kepala', 0.7, 0.2],
    ['Flu', 'Bersin-bersin', 0.6, 0.2],
    ['Flu', 'Batuk', 0.6, 0.1],
    ['Flu', 'Pilek, Hidung Buntu', 0.8, 0.1],
    ['Flu', 'Badan Lemas', 0.7, 0.1],
    ['Flu', 'Kedinginan', 0.8, 0.05]
]

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', gejala=gejala)

@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    gejala_dipilih = request.form.getlist('gejala')
    penyakit_terpilih = []
    list_cf = []

    for item in pengetahuan:
        if item[1] in gejala_dipilih and item[0] not in penyakit_terpilih:
            penyakit_terpilih.append(item[0])

    for p in penyakit_terpilih:
        mblama = mdlama = 0
        counter = 0
        for item in pengetahuan:
            if item[0] == p and item[1] in gejala_dipilih:
                mb = item[2]
                md = item[3]
                counter += 1
                if counter == 1:
                    mblama = mb
                    mdlama = md
                else:
                    mblama = (mblama + mb * (1 - mblama))
                    mdlama = (mdlama + md * (1 - mdlama))
        cf = round(mblama - mdlama, 4)
        list_cf.append({'penyakit': p, 'cf': cf})

    list_cf.sort(key=lambda x: x['cf'], reverse=True)

    return render_template('hasil.html', hasil=list_cf, gejala=gejala_dipilih)

if __name__ == '__main__':
    app.run(debug=True)
