## rpmbuild cannot create debuginfo
## for ada packages 
%global build_shared 1
Name:       florist    
Version:    2011
Release:    16%{?dist}
Summary:    Open-source implementation of IEEE Standard 1003.5b-1996
Group:      Development/Libraries
License:    GPLv2+
## Direct download not available
URL:        http://libre.adacore.com/libre/download2
Source0:    %{name}-gpl-%{version}-src.tgz
## Email ID : 20110802184724.GA8621@work.zhukoff.net
Patch0:     %{name}-shared.patch
## Fedora specific 
Patch3:     %{name}-fedora.patch
BuildRequires:  fedora-gnat-project-common >= 2
BuildRequires:  chrpath gprbuild autoconf gcc-gnat

# gcc-gnat only available on these:
ExclusiveArch: %GPRbuild_arches


%description
FLORIST is an implementation of the IEEE Standards 1003.5: 1992, 
IEEE STD 1003.5b: 1996, and parts of IEEE STD 1003.5c: 1998, 
also known as the POSIX Ada Bindings. Using this library, 
you can call operating system services from within Ada programs.

%package devel
Summary:    Devel package for florist
Group:      Development/Libraries
License:    GPLv2+
Requires:   fedora-gnat-project-common >= 2
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel 
%{summary}

%prep
%setup -q -n %{name}-gpl-%{version}-src
%patch0 -p1 
%patch3 -p1

%build
autoconf
%if %{build_shared}
%configure --enable-shared
%else
%configure --disable-shared
%endif
##%% export GNATOPTFLAGS="%GNAT_builder_flags"
make %{?_smp_mflags} GCCFLAGS='%{optflags}' GNATOPTFLAGS='%{GPRbuild_optflags}'


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} ADA_PROJECT_PATH="%_GNAT_project_dir" LIBDIR=%{_libdir}
%if %{build_shared}
chrpath --delete %{buildroot}/%{_libdir}/%{name}/libflorist.so.%{version}
chrpath --delete %{buildroot}/%{_libdir}/%{name}/libflorist.so
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README INSTALL
%dir %{_libdir}/%{name}
%if %{build_shared}
%{_libdir}/%{name}/libflorist.so.2011
%{_libdir}/libflorist.so.2011
%else
%{_libdir}/%{name}/libflorist.a
%endif

%files devel
%defattr(-,root,root,-)
%doc CHANGE_172259
%{_libdir}/%{name}/*.ali
%{_includedir}/%{name}
%{_GNAT_project_dir}/%{name}.gpr
%if %{build_shared}
%{_libdir}/%{name}/libflorist.so
%{_libdir}/libflorist.so
%endif

%changelog
* Sat Oct 11 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 2011-16
- Exclude arm 

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2011-13
- Use GNAT_arches rather than an explicit list

* Wed May  7 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 2011-12
- Rebuild with new libgnat

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jan 31 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 2011-10
- Add gcc-gnat to BR

* Sat Jan 26 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 2011-9
- Rebuild with new GCC-.48

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 2011-7
- Rebuild for new GCC-4.7

* Wed Aug 10 2011  Pavel Zhukov <landgraf@fedoraproject.org> - 2011-6
- Add ExclusiveArch

* Wed Aug 03 2011  Pavel Zhukov <landgraf@fedoraproject.org> - 2011-5
- Add posix-implemetation_signals
- Add posix-permissions_implementation

* Tue Aug 02 2011  Pavel Zhukov <landgraf@fedoraproject.org> - 2011-4
- Initial build
- Add C sources to *.so
- patch autoconf
