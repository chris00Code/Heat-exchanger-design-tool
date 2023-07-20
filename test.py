import matplotlib.pyplot as plt

# Beispiel-Daten
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Einen Linienplot erstellen
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Datenpunkte')

# Achsenbeschriftungen und Titel hinzufügen
plt.xlabel('X-Achse')
plt.ylabel('Y-Achse')
plt.title('Einfacher Testplot')

# Legende anzeigen
plt.legend()

# Plot anzeigen
plt.show()