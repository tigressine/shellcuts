scalaVersion := "2.11.12"
nativeLinkStubs := true
scalaSource in Compile := baseDirectory.value / "source"
scalaSource in Test := baseDirectory.value / "specs"
cleanFiles += baseDirectory.value / "pack"
libraryDependencies ++= Seq(
  "org.scalatest" % "scalatest_native0.3_2.11" % "3.2.0-SNAP10"
)

enablePlugins(ScalaNativePlugin)

lazy val programVersion = settingKey[String]("The program version.")
programVersion := "1.4.0"

lazy val supportedShells = settingKey[List[String]]("All supported shells.")
supportedShells := List("bash", "dash", "zsh", "ksh", "fish")

lazy val scrub = taskKey[Unit]("Cleans repo and removes additional junk.")
scrub := {
  import scala.sys.process._

  clean.value
  "rm -rf target/ project/project/ project/target/ dist/" !
}

lazy val prepack = taskKey[Unit]("Executes required tasks before packaging.")
prepack := Def.sequential(
  clean,
  Compile / nativeLink
).value

lazy val packDeb = taskKey[Unit]("Creates a Debian package.")
packDeb := {
  prepack.value

  import java.nio.charset.StandardCharsets
  import java.nio.file.{
    Files,
    Paths
  }
  import scala.sys.process._

  val packageName = s"shellcuts_${programVersion.value}-1"
  val installRoot = s"pack/${packageName}"

  // Create all required directories for the packaging process.
  val requiredDirs = List(
    "dist",
    s"${installRoot}/DEBIAN",
    s"${installRoot}/usr/bin",
    s"${installRoot}/etc/shellcuts/shells",
    s"${installRoot}/usr/share/man/man1",
    s"${installRoot}/usr/share/doc/shellcuts"
  )
  requiredDirs foreach {
    (path) => Files.createDirectories(Paths.get(path))
  }

  // Copy files into the packaging directory tree.
  val copies = Map(
    "scripts/sc" -> s"${installRoot}/usr/bin/sc",
    "target/scala-2.11/shellcuts-out" -> s"${installRoot}/usr/bin/sc-core",
    "docs/sc.1" -> s"${installRoot}/usr/share/man/man1/sc.1",
    "docs/CHANGES.txt" -> s"${installRoot}/usr/share/doc/shellcuts/CHANGES.txt",
    "docs/README.rst" -> s"${installRoot}/usr/share/doc/shellcuts/README.rst",
    "docs/LICENSE.txt" -> s"${installRoot}/usr/share/doc/shellcuts/LICENSE.txt",
    "shells/shellcuts.fish" -> s"${installRoot}/etc/shellcuts/shells/shellcuts.fish",
    "shells/shellcuts.sh" -> s"${installRoot}/etc/shellcuts/shells/shellcuts.sh"
  )
  copies foreach {
    case (source, destination) => {
      Files.copy(Paths.get(source), Paths.get(destination))
    }
  }

  // Create the required Debian control file for metadata.
  val controlContents = s"""
    |Package: shellcuts
    |Version: ${programVersion.value}-1
    |Section: base
    |Priority: optional
    |Architecture: amd64
    |Depends: libre2-dev
    |Maintainer: Tiger Sachse <tgsachse@gmail.com>
    |Description: Directory shortcuts for your shell
    |""".stripMargin.replaceFirst("\n", "")
  Files.write(
    Paths.get(s"${installRoot}/DEBIAN/control"),
    controlContents.getBytes(StandardCharsets.UTF_8)
  )

  // Build the deb package.
  s"dpkg-deb --build ${installRoot} dist/${packageName}.deb" !
}

lazy val pack = taskKey[Unit]("Packages this software.")
pack := Def.sequential(
  packDeb
).value

lazy val integrate = taskKey[Unit]("Executes the integration tests.")
integrate := {
  import scala.sys.process._

  val testSuites = List(
    "integ/new-flag-tests.sh",
    "integ/crumb-flag-tests.sh",
    "integ/delete-flag-tests.sh",
    "integ/follow-flag-tests.sh",
    "integ/unfollow-flag-tests.sh",
    "integ/move-flag-tests.sh"
  )

  val failed = supportedShells.value map {
    (shell) => {
      val functionSource = shell match {
        case "bash" | "dash" | "zsh" | "ksh" => {
          "/etc/shellcuts/shells/shellcuts.sh"
        }
        case "fish" => {
          "/etc/shellcuts/shells/shellcuts.fish"
        }
      }

      testSuites map {
        (suite) => s"${suite} ${shell} ${functionSource}" !
      } sum
    }
  } sum

  if (failed != 0) {
    throw new MessageOnlyException(s"$failed tests failed!")
  }
}
