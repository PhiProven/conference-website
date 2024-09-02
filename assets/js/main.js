---
---

{% include js/conference.js %}

window.conference.awaitReady().then(() => {
    const map = window.conference.map.getMap();

    if (typeof map !== 'undefined') {
        let main_entrance = L.marker([51.05638070648045, 3.7158354647654894], {
            icon: L.divIcon({
                className: '',
                html: '<span class="bg-light p-1 rounded-pill"><span class="fas fa-door-closed"></span> Het Rustpunt</span>',
                iconSize: [120, 56]
            })
        }).addTo(map);
        let back_entrance = L.marker([51.05784456914034, 3.7176827782455324], {
            icon: L.divIcon({
                className: '',
                html: '<span class="bg-light p-1 rounded-pill"><span class="fas fa-door-open"></span> Back entrance</span>',
                iconSize: [120, 56]
            })
        }).addTo(map);
        let zaal_entrance = L.marker([51.057711209520654, 3.7171706686829413], {
            icon: L.divIcon({
                className: '',
                html: '<span class="bg-light p-1 rounded-pill"><span class="fas fa-chalkboard"></span> Prinsenzaal</span>',
                iconSize: [120, 56]
            })
        }).addTo(map);
    }
});
