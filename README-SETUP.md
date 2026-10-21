# Εγκατάσταση του Jekyll βιογραφικού

1. Στο προσωπικό repository `vpetraki/my-cv-page` τοποθετήστε το `index.html`, `_config.yml` και `_data/cv.yml` στις αντίστοιχες θέσεις. Διατηρήστε το ήδη υπάρχον `vp_photo.jpg` στη ρίζα.
2. Στο **Settings → Pages**, επιλέξτε **Deploy from a branch**, `main`, `/(root)` εφόσον θέλετε την ενσωματωμένη υποστήριξη Jekyll του GitHub Pages. Αν έχετε ήδη workflow GitHub Actions για τη δημοσίευση, μην το αντικαταστήσετε χωρίς προηγούμενο έλεγχο· θα πρέπει να κάνει Jekyll build.
3. Αλλάζετε πλέον μόνο το `_data/cv.yml` για τα στοιχεία σας. Το Jekyll δημιουργεί την ορατή HTML στο build.
4. Η διεύθυνση παραμένει `https://vpetraki.github.io/my-cv-page/` με την προϋπόθεση ότι είναι σωστή η ρύθμιση Pages.

**Προσοχή:** Το αρχείο `index.html` θα περιέχει Liquid tags και δεν εμφανίζεται σωστά αν το ανοίξετε απευθείας τοπικά ή με απλό static hosting χωρίς Jekyll build. Η αυτόματη παραγωγή PDF με Pandoc + LaTeX είναι επόμενο, ξεχωριστό βήμα και δεν παρέχεται στο παρόν πακέτο.

Δοκιμή επανεκκίνησης GitHub Pages.
