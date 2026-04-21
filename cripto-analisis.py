!pip install fpdf2
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

respuesta = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1")
datos = respuesta.json()

nombres = [c['name'] for c in datos]
precios = [c['current_price'] for c in datos]
cambio_24h = [c['price_change_percentage_24h'] for c in datos]

df = pd.DataFrame({
    'cripto': nombres,
    'precio': precios,
    'cambio_24h': cambio_24h
})

print(df)
print(df.describe())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.bar(df['cripto'], df['precio'], color='gold')
ax1.set_title('Precios Actuales')
ax1.set_xticklabels(df['cripto'], rotation=90)

ax2.bar(df['cripto'], df['cambio_24h'], color=['green' if x > 0 else 'red' for x in df['cambio_24h']])
ax2.set_title('Cambio 24h %')
ax2.set_xticklabels(df['cripto'], rotation=90)

plt.tight_layout()
plt.show()

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", 'B', size=16)
pdf.cell(200, 10, txt="Reporte de Criptomonedas", ln=True, align='C')
pdf.ln(5)

pdf.set_font("Helvetica", size=11)
for _, fila in df.iterrows():
    pdf.cell(200, 8, txt=f"{fila['cripto']} - ${fila['precio']} - Cambio 24h: {round(fila['cambio_24h'], 2)}%", ln=True)

pdf.output("reporte_cripto.pdf")
print("Reporte PDF creado con éxito!")
