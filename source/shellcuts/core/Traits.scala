package shellcuts.core

trait Operation {
  def modify(configuration: Configuration,
             properties: List[String],
             parameters: List[String]):
             Either[String, Configuration]

  def command(configuration: Configuration,
              properties: List[String],
              parameters: List[String]):
              String
}
