%define	libname %mklibname %{name}
%define	devname %mklibname %{name} -d

#For git snapshots, set to 0 to use release instead:
%global snapshot 1
%if 0%{?snapshot}
	%global commitdate	20150821
	%global commit		b56fa78a2fe44ac2851bae5bf4f4693a0644da7b
	%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

Summary:	Compact Language Detector 2
Name:		cld2
Version:	20150820
Release:	%{?snapshot:0.git%{commitdate}.}1
License:	ASL 2.0
URL:		https://github.com/CLD2Owners/cld2/
Source0:	https://github.com/CLD2Owners/cld2/archive/%{?snapshot:%{commit}}%{!?snapshot:%{version}}/%{name}-%{?snapshot:%{shortcommit}}%{!?snapshot:%{version}}.tar.gz
# (debian)
Source1:	https://sources.debian.org/data/main/c/cld2/0.0.0-git20150806-9/CMakeLists.txt

BuildRequires:	cmake
BuildRequires:	ninja

%description
CLD2 probabilistically detects over 80 languages in Unicode UTF-8 text,
either plain text or HTML/XML.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
CLD2 probabilistically detects over 80 languages in Unicode UTF-8 text,
either plain text or HTML/XML.

%files -n %{libname}
%license LICENSE
%doc README.md
%{_libdir}/libcld2.so.*
%{_libdir}/libcld2_dynamic.so.*
%{_libdir}/libcld2_full.so.*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and libraries from %{name}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
CLD2 probabilistically detects over 80 languages in Unicode UTF-8 text,
either plain text or HTML/XML.

Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%doc docs/*
%{_includedir}/%{name}
%{_libdir}/libcld2.so
%{_libdir}/libcld2_dynamic.so
%{_libdir}/libcld2_full.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}

# CMakeLists.txt
cp %{SOURCE1} .

%build
# https://github.com/CLD2Owners/cld2/issues/47
export CXXFLAGS="%{optflags} -std=c++98"

%cmake \
	-GNinja
%ninja_build

%install
%ninja_install -C build

