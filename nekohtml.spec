Summary:	HTML scanner and tag balancer
Name:		nekohtml
Version:	0.9.5
Release:	0.1
License:	Apache-like
URL:		http://www.apache.org/~andyc/neko/doc/html/
Source0:	http://www.apache.org/~andyc/neko/%{name}-%{version}.tar.gz
# Source0-md5:	a5b22b189f23d0648eabc308fcfd4542
Source1:	%{name}-filter.sh
Patch0:		%{name}-crosslink.patch
Patch1:		%{name}-HTMLScanner.patch
Group:		Applications/Text
BuildRequires:	jakarta-ant
# for javadoc
BuildRequires:	java-sun
BuildRequires:	xerces-j >= 2.3.0
Requires:	xerces-j >= 2.3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NekoHTML is a simple HTML scanner and tag balancer that enables
application programmers to parse HTML documents and access the
information using standard XML interfaces. The parser can scan HTML
files and "fix up" many common mistakes that human (and computer)
authors make in writing HTML documents. NekoHTML adds missing parent
elements; automatically closes elements with optional end tags; and
can handle mismatched inline element tags. NekoHTML is written using
the Xerces Native Interface (XNI) that is the foundation of the
Xerces2 implementation. This enables you to use the NekoHTML parser
with existing XNI tools without modification or rewriting code.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:	Demo for %{name}
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -b .sav
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath xerces-j2)
ant -f build-html.xml \
	-Djarfile=%{name}-%{version}.jar \
	-DjarfileXni=%{name}-xni-%{version}.jar \
	-DjarfileSamples=%{name}-samples-%{version}.jar \
	-Dj2se.javadoc=%{_javadocdir}/java \
	-Dxni.javadoc=%{_javadocdir}/xerces-j2-xni \
	-Dxerces.javadoc=%{_javadocdir}/xerces-j2-impl \
	clean package jar-xni test

%install
rm -rf $RPM_BUILD_ROOT

# Jars
install -d $RPM_BUILD_ROOT%{_javadir}
install -p %{name}{,-xni}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-xni-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xni.jar

# Scripts
install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}-filter

# Samples
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p %{name}-samples-%{version}.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/

# Javadocs
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr bin/package/nekohtml-*/doc/html/javadoc/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# Avoid having javadocs in %doc.
rm -rf bin/package/nekohtml-*/doc/html/javadoc

# Fix link between docs and javadoc.
cd bin/package/nekohtml-*/doc/html
ln -sf %{_javadocdir}/%{name}-%{version} javadoc

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE* README* TODO* bin/package/nekohtml-*/doc/*
%attr(755,root,root) %{_bindir}/%{name}-filter
%{_javadir}/%{name}*.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}-%{version}