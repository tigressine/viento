# Maintainer: tgsachse (Tiger Sachse) <tgsachse@gmail.com>
pkgname=viento-git
pkgver=0.3.0
pkgrel=1

pkgdesc="Daemon and CLI interface for cloud storage management."
arch=('any')
url="https://github.com/tgsachse/viento"
license=('GPLv3')
depends=('python' 'rclone' 'python-termcolor')
source=('git+https://github.com/tgsachse/viento.git')

pkgver(){
    cd viento
    git describe --long | sed 's/^v-//;s/\([^-]*-g\)/r\1/;s/-/./g'
}


package() {
    cd viento
	install -Dm 0777 -t ${pkgdir}/usr/bin viento
    install -Dm 0777 -t "${pkgdir}/usr/lib/python3.6/site-packages" viento_s.py viento_d.py 
}
