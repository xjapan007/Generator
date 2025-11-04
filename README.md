# Générateur de Combos

Un outil de bureau (créé avec Tkinter) pour générer des listes de combinaisons "utilisateur:mot de passe" (combos) avec de nombreuses options de personnalisation.

![Image de l'application](https://i.imgur.com/siEtCNx.png)

---

## 🚀 Fonctionnalités

* **Génération de Combos** : Créez des listes au format `utilisateur:mot de passe`.
* **Personnalisation Complète** :
    * Choisissez la longueur du nom d'utilisateur et du mot de passe.
    * Sélectionnez le type de caractères (numérique, alphabétique, alphanumérique).
    * Incluez ou non des caractères spéciaux.
    * Ajoutez des préfixes et des suffixes.
* **Mode Fixe** : Possibilité de fixer le nom d'utilisateur ou le mot de passe à une valeur spécifique.
* **Interface Graphique** :
    * Interface claire basée sur des onglets (Générateur, Paramètres).
    * Personnalisation des couleurs (RGB) du texte, du user et du pass dans l'aperçu.
    * Barre de progression en temps réel.
* **Export Facile** : Sauvegardez vos listes de combos générées en `.txt` ou en `.xlsx` (Excel).

---

## 🛠️ Utilisation

Il y a deux façons d'utiliser cet outil :

### 1. Version Exécutable (.exe)

Vous pouvez télécharger la dernière version compilée (le fichier `.exe`) directement depuis la [section Releases](https://github.com/xjapan007/Generator/releases) de ce dépôt.


### 2. Depuis le code source

Si vous avez Python installé, vous pouvez lancer le script directement.

1.  **Clonez le dépôt :**
    ```bash
    git clone [https://github.com/xjapan007/Generator.git](https://github.com/xjapan007/Generator.git)
    cd VOTRE_REPO
    ```

2.  **(Recommandé) Créez un environnement virtuel :**
    ```bash
    python -m venv venv
    ```
    * Sur Windows : `venv\Scripts\activate`
    * Sur macOS/Linux : `source venv/bin/activate`

3.  **Installez les dépendances :**
    L'outil utilise `openpyxl` pour l'export Excel.
    ```bash
    pip install openpyxl
    ```

4.  **Lancez l'application :**
    ```bash
    python generator.py
    ```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une *issue* pour signaler un bug ou proposer une amélioration, ou à soumettre une *pull request*.


## ❤️ Soutenir le projet

Si ce projet vous est utile et que vous souhaitez me remercier, vous pouvez m'offrir un café !

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P21NKY2H)

---

## 📄 License

This project is licensed under the MIT License.