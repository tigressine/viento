# Maintainer: tgsachse (Tiger Sachse) <tgsachse@gmail.com>
pkgname=Wind
pkgver=0.2.0
pkgrel=1

pkgdesc="Daemon and CLI interface for cloud storage management."
arch=('any')
url="https://github.com/tgsachse/Wind"
license=('GPL')
depends=('python>=3.3.0' 'rclone>=1.36')
source=('https://github.com/tgsachse/Wind.git')

package() {
	cd "$pkgdir"
	install -Dm 0777 -t ${pkgdir}/usr/bin wind wind_setup.py wind_daemon.py 
}
