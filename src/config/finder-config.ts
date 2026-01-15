export class FinderConfig {
  public pattern = `[ ,-.{_(\"'<\\[\t]`;
  public skipSelection = false;
  public onlyInitialLetter = true;
  public includeEndCharInSelection = true;
  public jumpToLineEndings = false;
  public jumpToEndOfWord = false;
  public mode: 'char' | 'regex' = 'char';
  public disableOnlyInitialLetterInRegex = true;
  // Mapping from input character to regex pattern for alternative matches
  public charRegexMap: Record<string, string> = {};
}
