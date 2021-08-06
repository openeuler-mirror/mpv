Name:           mpv
Version:        0.32.0
Release:        1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+ and LGPLv2+
URL:            http://mpv.io/
Source0:        https://github.com/mpv-player/mpv/archive/v%{version}/%{name}-%{version}.tar.gz

# set defaults for Fedora
Patch0:         %{name}-config.patch

# Fix ppc as upstream refuse to fix the issue
# https://github.com/mpv-player/mpv/issues/3776
Patch1:         ppc_fix.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enca)
BuildRequires:  pkgconfig(libavutil) >= 56.12.100
BuildRequires:  pkgconfig(libavcodec) >= 58.16.100
BuildRequires:  pkgconfig(libavformat) >= 58.9.100
BuildRequires:  pkgconfig(libswscale) >= 5.0.101
BuildRequires:  pkgconfig(libavfilter) >= 7.14.100
BuildRequires:  pkgconfig(libswresample) >= 3.0.100
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(mujs)
BuildRequires:  pkgconfig(uchardet) >= 0.0.5
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(libguess)

BuildRequires:  pkgconfig(vulkan)

BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive) >= 3.4.0
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libquvi-0.9)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(luajit)

BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zimg)
# Requires zimg version >= 2.9
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-docutils
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Encode)
BuildRequires:  waf

# Obsoletes older ci/cd
Obsoletes:  mpv-master < %{version}-100
Provides:   mpv-master = %{version}-100

Requires:       hicolor-icon-theme
Provides:       mplayer-backend

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package libs
Summary: Dynamic library for Mpv frontends 

%description libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package libs-devel
Summary: Development package for libmpv
Requires: mpv-libs%{?_isa} = %{version}-%{release}

%description libs-devel
Libmpv development header files and libraries.

%prep
%autosetup -p1 -n mpv-%{?commit}%{?!commit:%{version}}

sed -i -e "s|c_preproc.standard_includes.append('/usr/local/include')|c_preproc.standard_includes.append('$(pkgconf --variable=includedir libavcodec)')|" wscript


%build
%set_build_flags
%{_bindir}/waf configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/%{name} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --enable-libmpv-shared \
    --enable-sdl2 \
    --enable-libarchive \
    --enable-libsmbclient \
    --enable-dvdnav \
    --enable-cdda \
    --enable-html-build \
    --disable-vaapi \
    --enable-dvbin
    

%{_bindir}/waf -v build %{?_smp_mflags}

%install
%{_bindir}/waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}/

%files
%docdir %{_docdir}/%{name}/
%{_docdir}/%{name}/
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_datadir}/zsh/site-functions/_mpv
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}/
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Thu May 13 2021 He Rengui <herengui@uniontech.com> - 0.32.0-1
- package init
