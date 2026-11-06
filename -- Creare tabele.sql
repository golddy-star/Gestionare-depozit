-- Creare tabele
CREATE TABLE categorii (id SERIAL PRIMARY KEY, nume VARCHAR(100) NOT NULL, descriere TEXT);

CREATE TABLE furnizori (id SERIAL PRIMARY KEY, nume_companie VARCHAR(150) NOT NULL, persoana_contact VARCHAR(100), telefon VARCHAR(20), email VARCHAR(100));

CREATE TABLE produse (id SERIAL PRIMARY KEY, cod_sku VARCHAR(50) UNIQUE NOT NULL, nume VARCHAR(200) NOT NULL, categorie_id INT REFERENCES categorii(id) ON DELETE SET NULL, furnizor_id INT REFERENCES furnizori(id) ON DELETE SET NULL, pret_unitar NUMERIC(10, 2) NOT NULL, data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE locatii_depozit (id SERIAL PRIMARY KEY, cod_locatie VARCHAR(50) UNIQUE NOT NULL, zona VARCHAR(50) NOT NULL, raft VARCHAR(50) NOT NULL);

CREATE TABLE stocuri (id SERIAL PRIMARY KEY, produs_id INT REFERENCES produse(id) ON DELETE CASCADE, locatie_id INT REFERENCES locatii_depozit(id) ON DELETE CASCADE, cantitate INT DEFAULT 0, ultima_actualizare TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(produs_id, locatie_id));

CREATE TABLE tranzactii_marfa (id SERIAL PRIMARY KEY, produs_id INT REFERENCES produse(id) ON DELETE CASCADE, tip_tranzactie VARCHAR(20) CHECK (tip_tranzactie IN ('INTRARE', 'IESIRE')), cantitate INT NOT NULL, data_tranzactie TIMESTAMP DEFAULT CURRENT_TIMESTAMP, observatii TEXT);

-- Adaugare date de test
INSERT INTO categorii (nume) VALUES ('Electronice'), ('Birotica');
INSERT INTO furnizori (nume_companie) VALUES ('TechCorp SRL'), ('OfficeSupplies SA');
INSERT INTO produse (cod_sku, nume, categorie_id, furnizor_id, pret_unitar) VALUES ('SKU-001', 'Laptop Dell XPS', 1, 1, 7500.00), ('SKU-002', 'Hartie A4', 2, 2, 25.50);
INSERT INTO locatii_depozit (cod_locatie, zona, raft) VALUES ('Z1-R1', 'Zona 1', 'Raft 1'), ('Z1-R2', 'Zona 1', 'Raft 2');
INSERT INTO stocuri (produs_id, locatie_id, cantitate) VALUES (1, 1, 10), (2, 2, 500);