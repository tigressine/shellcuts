package shellcuts.core

import java.nio.charset.Charset
import scala.util.matching.Regex

object Encoding {
  def decode(globalsPattern: Regex, shellcutPattern: Regex, pathPattern: Regex)
            (encoded: String):
            Configuration = {

    val (crumb, defaultFollow) = globalsPattern.findFirstIn(encoded) map {
      case globalsPattern(crumb, defaultFollow) => {
        (Option(crumb), Option(defaultFollow))
      }
    } getOrElse((None, None))

    val shellcuts = shellcutPattern.findAllIn(encoded).toList map {
      case shellcutPattern(name, follow, paths) => {
        Shellcut(
          name,
          Option(follow),
          pathPattern.findAllIn(paths).toList map {
            case pathPattern(path) => path
          }
        )
      }
    }

    Configuration(crumb, defaultFollow, shellcuts)
  }

  def encode(bigDelimiter: String,
             smallDelimiter: String,
             charset: Charset)
            (configuration: Configuration):
            String = {

    val globals = configuration.crumb.getOrElse("") +
      smallDelimiter +
      configuration.defaultFollow.getOrElse("")

    val shellcuts = configuration.shellcuts map {
      (shellcut) => {
        (shellcut.name :: shellcut.follow.getOrElse("") :: shellcut.paths)
          .mkString(smallDelimiter)
      }
    } mkString(bigDelimiter)

    globals + bigDelimiter + shellcuts
  }
}
